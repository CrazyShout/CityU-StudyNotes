"""Deterministic numerical checks and original teaching figures for CS5489 Lectures 10, 11, and 12."""
from pathlib import Path
import json
import os

D = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(D / '.cache/matplotlib'))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import softmax

plt.rcParams.update({
    'font.size': 10.5,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

checks = {}


def record(name, actual, expected, rtol=1e-6, atol=1e-7):
    assert np.allclose(actual, expected, rtol=rtol, atol=atol), (name, actual, expected)
    checks[name] = {
        'actual': np.asarray(actual).tolist(),
        'expected': np.asarray(expected).tolist(),
    }


def save(fig, name):
    fig.tight_layout()
    fig.savefig(D / 'assets' / name, dpi=160, bbox_inches='tight')
    plt.close(fig)


# =============================================================================
# LECTURE 10 NUMERICAL VERIFICATIONS
# =============================================================================

# 1. Reparameterization & change-of-variables PDF: y = 2z - 1, z ~ N(0, 1) => y ~ N(-1, 4)
y_test = np.array([-3.0, -1.0, 1.0, 3.0])
z_inv = (y_test + 1.0) / 2.0
p_z = np.exp(-0.5 * z_inv ** 2) / np.sqrt(2.0 * np.pi)
p_y_cov = 0.5 * p_z
p_y_direct = np.exp(-0.5 * ((y_test + 1.0) ** 2) / 4.0) / np.sqrt(2.0 * np.pi * 4.0)
record('l10_change_of_vars_pdf', p_y_cov, p_y_direct)

# 2. VAE closed-form Gaussian KL(N(mu, sigma^2) || N(0, 1))
def kl_gauss_std(mu, sigma):
    return 0.5 * (mu ** 2 + sigma ** 2 - 1.0 - np.log(sigma ** 2))

record('l10_vae_kl', [kl_gauss_std(0.0, 1.0), kl_gauss_std(1.0, 2.0)], [0.0, 2.0 - np.log(2.0)])

# 3. GAN optimal discriminator & minimax vs non-saturating generator logit gradient
# Suppose D(x) = sigmoid(u).
# Minimax G loss: L_mm = log(1 - sigmoid(u)) -> dL_mm/du = -sigmoid(u) = -D
# Non-saturating G loss: L_ns = -log(sigmoid(u)) -> dL_ns/du = -(1 - sigmoid(u)) = -(1 - D)
D_early = 0.01  # discriminator easily rejects early fake sample
grad_mm_early = -D_early           # -0.01 (vanishing!)
grad_ns_early = -(1.0 - D_early)   # -0.99 (strong gradient!)
record('l10_gan_grads_early', [abs(grad_mm_early), abs(grad_ns_early)], [0.01, 0.99])
record('l10_gan_equilibrium_loss', np.log(0.5) + np.log(0.5), -np.log(4.0))

# 4. Diffusion 2-step forward marginal & CFG linear combination
beta1, beta2 = 0.1, 0.1
alpha_bar_2 = (1.0 - beta1) * (1.0 - beta2)
record('l10_diffusion_alpha_bar', [alpha_bar_2, np.sqrt(alpha_bar_2), 1.0 - alpha_bar_2], [0.81, 0.9, 0.19])
eps_u, eps_c = np.array([1.0, -0.5]), np.array([1.4, -0.1])
cfg_75 = eps_u + 7.5 * (eps_c - eps_u)
record('l10_cfg_scale_7_5', cfg_75, [4.0, 2.5])


# =============================================================================
# LECTURE 11 NUMERICAL VERIFICATIONS
# =============================================================================

# 1. Bigram LM & Perplexity (exact match to Lecture 11a c013-c014)
# Corpus: ["I", "am", "a", "student"], ["I", "study", "LLM"], ["LLM", "is", "cool"]
# Test seq: ["I", "am", "a", "student", "<EOS>"]
# Bigram probs: P(I|<BOS>)=2/3, P(am|I)=1/2, P(a|am)=1, P(student|a)=1, P(<EOS>|student)=1
probs_seq = np.array([2.0 / 3.0, 0.5, 1.0, 1.0, 1.0])
nll_bits = -np.mean(np.log2(probs_seq))
ppl = 2.0 ** nll_bits
record('l11_bigram_nll_ppl', [nll_bits, ppl], [0.31699250014423125, 1.2457309396155174])

# 2. Next-token NLL (natural log, matching Lecture 11b c009)
record('l11_token_ce', [-np.log(0.8), -np.log(0.1)], [0.2231435513142097, 2.3025850929940455])

# 3. Decoding worked examples (exact match to Lecture 11b c021)
record('l11_greedy_vs_best_path', [0.6 * 0.5, 0.4 * 0.95], [0.30, 0.38])
p5 = np.array([0.40, 0.30, 0.15, 0.10, 0.05])
topk2 = p5[:2] / p5[:2].sum()
topp08 = p5[:3] / p5[:3].sum()  # cumsum = [0.40, 0.70, 0.85] -> first 3
# Order matters: top-k=3 first gives [8/17, 6/17, 3/17]; cumsum[:2] = 14/17 = 0.8235 >= 0.8 -> keeps only 2!
topk3_then_p08 = topp08[:2] / topp08[:2].sum()
record('l11_topk2', topk2, [4.0 / 7.0, 3.0 / 7.0])
record('l11_topp08', topp08, [8.0 / 17.0, 6.0 / 17.0, 3.0 / 17.0])
record('l11_topk3_then_topp08', topk3_then_p08, [4.0 / 7.0, 3.0 / 7.0])

# 4. GRPO group-relative advantages (matching Lecture 11b c017)
rewards = np.array([1.0, 0.0, 0.0, 0.0])
adv = (rewards - rewards.mean()) / rewards.std()
record('l11_grpo_advantages', adv, [np.sqrt(3.0), -1.0 / np.sqrt(3.0), -1.0 / np.sqrt(3.0), -1.0 / np.sqrt(3.0)])


# =============================================================================
# LECTURE 12 NUMERICAL VERIFICATIONS
# =============================================================================

# 1. RoPE 2D relative position invariance: (R(m*th) q)^T (R(n*th) k) == q^T R((n-m)*th) k
def rot2d(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s], [s, c]])

q_v = np.array([1.5, -0.7])
k_v = np.array([0.4, 2.1])
th = 0.35
dot_m2_n5 = (rot2d(2 * th) @ q_v) @ (rot2d(5 * th) @ k_v)
dot_m10_n13 = (rot2d(10 * th) @ q_v) @ (rot2d(13 * th) @ k_v)
dot_rel3 = q_v @ (rot2d(3 * th) @ k_v)
record('l12_rope_relative_invariance', [dot_m2_n5, dot_m10_n13], [dot_rel3, dot_rel3])

# 2. RPN anchors & YOLO output tensor dimensions & ViT patch counts
record('l12_rpn_yolo_vit_counts',
       [14 * 14 * 9, 7 * 7 * (20 + 2 * 5), (224 // 32) ** 2, (224 // 16) ** 2],
       [1764, 1470, 49, 196])

# 3. Triplet loss worked check
d_ap, d_an1, d_an2, margin = 0.2, 0.5, 1.0, 0.5
record('l12_triplet_loss',
       [max(d_ap - d_an1 + margin, 0.0), max(d_ap - d_an2 + margin, 0.0)],
       [0.2, 0.0])

# 4. CLIP symmetric InfoNCE loss on 2x2 cosine similarity matrix
# Aligned unit vectors vs orthogonal off-diagonals: S = [[1, 0], [0, 1]], tau = 0.5 => logits = [[2, 0], [0, 2]]
tau_clip = 0.5
S_clip = np.array([[1.0, 0.0], [0.0, 1.0]])
logits_clip = S_clip / tau_clip
p_row = softmax(logits_clip, axis=1)
p_col = softmax(logits_clip, axis=0)
loss_i2t = -np.mean(np.log(np.diag(p_row)))
loss_t2i = -np.mean(np.log(np.diag(p_col)))
loss_sym = 0.5 * (loss_i2t + loss_t2i)
expected_ce = np.log(1.0 + np.exp(-2.0))
record('l12_clip_symmetric_loss', [loss_i2t, loss_t2i, loss_sym], [expected_ce] * 3)


# =============================================================================
# ORIGINAL TEACHING FIGURES (CLEAN, ENGLISH-LABELED, REPRODUCIBLE)
# =============================================================================

# Figure 1 (Lecture 10): VAE Reparameterization Trick + GAN Minimax vs Non-saturating Gradient
fig, axs = plt.subplots(1, 2, figsize=(10.0, 3.6), gridspec_kw={'width_ratios': [1.1, 1.0]})

# Left: VAE Reparameterization schematic
ax = axs[0]
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.2)
ax.axis('off')
ax.set_title('VAE Reparameterization Trick ($z = \\mu + \\sigma \\odot \\epsilon$)', fontsize=10.0)

def draw_box(ax_, xy, w, h, text, fc='#eef2f5', ec='#456b8d', tc='#1d3549', fs=8.8):
    rect = plt.Rectangle(xy, w, h, facecolor=fc, edgecolor=ec, lw=1.4, zorder=3)
    ax_.add_patch(rect)
    ax_.text(xy[0] + w / 2, xy[1] + h / 2, text, ha='center', va='center', fontsize=fs, color=tc, zorder=4)

draw_box(ax, (0.2, 2.0), 1.3, 1.1, 'Input\n$\\mathbf{x}$', fc='#eef2f5', ec='#456b8d')
draw_box(ax, (2.1, 1.8), 1.7, 1.5, 'Encoder\nNN', fc='#dce7f0', ec='#2c4863')
draw_box(ax, (4.4, 2.9), 1.3, 0.9, '$\\boldsymbol{\\mu}(\\mathbf{x})$', fc='#e7f1ee', ec='#448775', tc='#1f473c')
draw_box(ax, (4.4, 1.4), 1.3, 0.9, '$\\boldsymbol{\\sigma}(\\mathbf{x})$', fc='#e7f1ee', ec='#448775', tc='#1f473c')
draw_box(ax, (4.3, 0.1), 1.5, 0.85, '$\\boldsymbol{\\epsilon}\\sim\\mathcal{N}(0,I)$', fc='#f6ece8', ec='#a45b44', tc='#6e3523', fs=8.2)
draw_box(ax, (6.3, 2.0), 1.3, 1.1, '$\\mathbf{z}=\\boldsymbol{\\mu}+$\n$\\boldsymbol{\\sigma}\\odot\\boldsymbol{\\epsilon}$', fc='#f4efd9', ec='#93764b', tc='#5a4525', fs=8.3)
draw_box(ax, (8.1, 1.8), 1.7, 1.5, 'Decoder\n$\\hat{\\mathbf{x}}=g(\\mathbf{z})$', fc='#dce7f0', ec='#2c4863')

arr_kw = dict(arrowstyle='->', lw=1.4, color='#334455')
ax.annotate('', xy=(2.1, 2.55), xytext=(1.5, 2.55), arrowprops=arr_kw)
ax.annotate('', xy=(4.4, 3.35), xytext=(3.8, 2.85), arrowprops=arr_kw)
ax.annotate('', xy=(4.4, 1.85), xytext=(3.8, 2.25), arrowprops=arr_kw)
ax.annotate('', xy=(6.3, 2.85), xytext=(5.7, 3.30), arrowprops=arr_kw)
ax.annotate('', xy=(6.3, 2.35), xytext=(5.7, 1.85), arrowprops=arr_kw)
ax.annotate('', xy=(6.95, 2.0), xytext=(5.8, 0.55), arrowprops=dict(arrowstyle='->', lw=1.4, ls='--', color='#a45b44'))
ax.annotate('', xy=(8.1, 2.55), xytext=(7.6, 2.55), arrowprops=arr_kw)
ax.text(5.0, 4.45, 'Backprop flows smoothly through $\\mu, \\sigma$\n(randomness $\\epsilon$ is an external input)',
        ha='center', va='center', fontsize=8.4, color='#2c4863',
        bbox=dict(boxstyle='round,pad=0.3', fc='#f8fafb', ec='#c3d0da'))

# Right: GAN generator gradient magnitude wrt discriminator logit u as D(G(z)) varies
ax2 = axs[1]
d_vals = np.linspace(0.01, 0.99, 200)
# |dL/du| for minimax log(1-D) is D; for non-saturating -log(D) is 1-D
ax2.plot(d_vals, d_vals, '--', color='#a45b44', lw=2.0, label='Minimax: $\\min_G\\,\\log(1-D(G(z)))$')
ax2.plot(d_vals, 1.0 - d_vals, '-', color='#456b8d', lw=2.2, label='Non-saturating: $\\min_G\\,-\\log D(G(z))$')
ax2.axvline(0.05, color='#448775', ls=':', lw=1.3)
ax2.text(0.08, 0.52, 'Early training:\n$D(G(z))\\approx 0$\nMinimax gradient\nvanishes!', fontsize=8.2, color='#2d5f51',
         bbox=dict(facecolor='white', edgecolor='none', alpha=0.88, pad=1.5))
ax2.set_xlabel('Discriminator score $D(G(z))$ on fake sample')
ax2.set_ylabel('$|\\partial \\mathcal{L}_G / \\partial u|$ (logit gradient mag.)')
ax2.set_title('Why Non-Saturating GAN Loss Trains Better', fontsize=10.0)
ax2.grid(alpha=0.2)
ax2.legend(fontsize=7.8, loc='lower center', frameon=True, framealpha=0.92)
save(fig, 'l10-generative-models.png')


# Figure 2 (Lecture 11): Decoding distribution reshaping + Causal attention mask / KV cache
fig, axs = plt.subplots(1, 2, figsize=(9.8, 3.6), gridspec_kw={'width_ratios': [1.25, 0.95]})

# Left: Temperature / Top-k / Top-p comparison on 5 tokens
ax = axs[0]
toks = ['$v_1$', '$v_2$', '$v_3$', '$v_4$', '$v_5$']
logits5 = np.log(p5)
p_t05 = softmax(logits5 / 0.5)
p_t20 = softmax(logits5 / 2.0)
p_topp = np.array([8/17, 6/17, 3/17, 0.0, 0.0])
x_i = np.arange(5)
w = 0.20
ax.bar(x_i - 1.5 * w, p5, w, color='#456b8d', label='Base ($\\tau=1$)')
ax.bar(x_i - 0.5 * w, p_t05, w, color='#2c4863', label='Sharp ($\\tau=0.5$)')
ax.bar(x_i + 0.5 * w, p_t20, w, color='#93764b', label='Flat ($\\tau=2.0$)')
ax.bar(x_i + 1.5 * w, p_topp, w, color='#448775', label='Top-$p=0.8$ (3 kept)')
ax.set_xticks(x_i)
ax.set_xticklabels(toks)
ax.set_ylim(0, 0.68)
ax.set_ylabel('Next-token probability')
ax.set_title('Decoding: Temperature & Top-$p$ Filtering', fontsize=10.0)
ax.grid(axis='y', alpha=0.2)
ax.legend(fontsize=7.9, loc='upper right')

# Right: Causal attention matrix + Prefill vs Decode KV cache
ax2 = axs[1]
n_seq = 5
mat = np.zeros((n_seq, n_seq))
for r in range(n_seq):
    for c in range(n_seq):
        if c > r:
            mat[r, c] = 0.0   # masked future
        elif r < 3:
            mat[r, c] = 1.0   # prefill (prompt tokens 1..3)
        else:
            mat[r, c] = 2.0   # decode steps reusing cached K,V
from matplotlib.colors import ListedColormap
cmap = ListedColormap(['#f2f2f2', '#456b8d', '#448775'])
ax2.imshow(mat, cmap=cmap, vmin=0, vmax=2)
labels_tok = ['$q_1$', '$q_2$', '$q_3$', '$y_1$', '$y_2$']
ax2.set_xticks(range(n_seq))
ax2.set_yticks(range(n_seq))
ax2.set_xticklabels([f'K,V {t}' for t in labels_tok], fontsize=8.3)
ax2.set_yticklabels([f'Q {t}' for t in labels_tok], fontsize=8.3)
for r in range(n_seq):
    for c in range(n_seq):
        txt = '$-\\infty$' if c > r else ('Pre' if r < 3 else 'Dec')
        col = '#999999' if c > r else 'white'
        ax2.text(c, r, txt, ha='center', va='center', fontsize=8.0, color=col)
ax2.set_title('Causal Mask: Prefill vs Decode (KV Cache)', fontsize=10.0)
save(fig, 'l11-decoding-kvcache.png')


# Figure 3 (Lecture 12): Object Detection paradigm comparison + CLIP N x N symmetric contrastive matrix
fig, axs = plt.subplots(1, 2, figsize=(9.8, 3.6), gridspec_kw={'width_ratios': [1.25, 0.95]})

# Left: Detector architectural comparison schematic
ax = axs[0]
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.2)
ax.axis('off')
ax.set_title('Object Detection Evolution (2-Stage vs 1-Stage vs DETR)', fontsize=9.8)
rows_det = [
    (4.1, 'R-CNN', 'Selective Search -> Crop -> CNN per RoI -> SVM + Box', '#a45b44'),
    (3.1, 'Fast R-CNN', 'CNN once on image -> RoI Pooling -> Cls + Box', '#93764b'),
    (2.1, 'Faster R-CNN', 'CNN -> RPN (k=9 anchors) -> RoI Head (end-to-end)', '#456b8d'),
    (1.1, 'YOLO (1-stage)', 'S x S grid directly outputs S x S x (C + 5B)', '#448775'),
    (0.1, 'DETR', 'CNN + Transformer + Object Queries + Hungarian Match', '#2c4863'),
]
for y0, name, desc, col in rows_det:
    ax.add_patch(plt.Rectangle((0.1, y0), 2.35, 0.72, facecolor=col, edgecolor='none', zorder=3))
    ax.text(1.275, y0 + 0.36, name, ha='center', va='center', fontsize=8.3, color='white', fontweight='bold', zorder=4)
    ax.add_patch(plt.Rectangle((2.55, y0), 7.35, 0.72, facecolor='#f5f7f9', edgecolor='#c7d1da', lw=1.0, zorder=3))
    ax.text(2.75, y0 + 0.36, desc, ha='left', va='center', fontsize=8.1, color='#222222', zorder=4)

# Right: CLIP N x N similarity matrix (diagonal = matched pairs)
ax2 = axs[1]
sim = np.array([
    [0.92, 0.14, 0.08, 0.11],
    [0.12, 0.89, 0.18, 0.09],
    [0.09, 0.16, 0.94, 0.15],
    [0.10, 0.07, 0.13, 0.91],
])
im = ax2.imshow(sim, cmap='Blues', vmin=0.0, vmax=1.0)
ax2.set_xticks(range(4))
ax2.set_yticks(range(4))
ax2.set_xticklabels(['$T_1$', '$T_2$', '$T_3$', '$T_4$'])
ax2.set_yticklabels(['$I_1$', '$I_2$', '$I_3$', '$I_4$'])
ax2.set_xlabel('Text embeddings $\\mathbf{u}_j$ (normalized)')
ax2.set_ylabel('Image embeddings $\\mathbf{z}_i$')
for i in range(4):
    for j in range(4):
        lbl = 'pos' if i == j else 'neg'
        col = 'white' if i == j else '#445566'
        ax2.text(j, i, f'{sim[i,j]:.2f}\n({lbl})', ha='center', va='center', fontsize=7.6, color=col)
ax2.set_title('CLIP Contrastive Matrix ($\\mathbf{z}_i^\\top \\mathbf{u}_j / \\tau$)', fontsize=9.8)
save(fig, 'l12-detectors-clip.png')

(D / 'l10-l12-example-results.json').write_text(json.dumps(checks, indent=2) + '\n')
print(f'All {len(checks)} checks passed and 3 figures generated.')
