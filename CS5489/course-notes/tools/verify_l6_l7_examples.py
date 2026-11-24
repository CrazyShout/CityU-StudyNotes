"""Deterministic numerical checks and original teaching figures for CS5489 Lectures 6 and 7."""
from pathlib import Path
import json
import math
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
# LECTURE 6 NUMERICAL VERIFICATIONS
# =============================================================================

# 1. 1D discrete convolution: full / same / valid + Toeplitz matrix equivalence
x = np.array([1.0, 2.0, 3.0, 2.0, 1.0])
w = np.array([1.0, 0.0, -1.0])  # finite-difference / edge detector kernel
s_full = np.convolve(x, w, mode='full')
s_same = np.convolve(x, w, mode='same')
s_valid = np.convolve(x, w, mode='valid')
record('l6_conv1d_full', s_full, [1., 2., 2., 0., -2., -2., -1.])
record('l6_conv1d_same', s_same, [2., 2., 0., -2., -2.])
record('l6_conv1d_valid', s_valid, [2., 0., -2.])
record('l6_conv1d_lengths', [len(s_full), len(s_same), len(s_valid)], [7, 5, 3])

# Toeplitz matrix A^T matching 'same' mode for w = [w1, w2, w3]
A_T = np.array([
    [w[1], w[0], 0.,   0.,   0.],
    [w[2], w[1], w[0], 0.,   0.],
    [0.,   w[2], w[1], w[0], 0.],
    [0.,   0.,   w[2], w[1], w[0]],
    [0.,   0.,   0.,   w[2], w[1]],
])
# Wait: check definition of convolution s[n] = sum_k x[k] w[n - k]:
# For 'same' center index offset = 1:
# s_same[0] = x[0]*w[1] + x[1]*w[0] -> WAIT! Let's check:
# s_full[0] = x[0]*w[0] = 1
# s_full[1] = x[0]*w[1] + x[1]*w[0] = 0 + 2 = 2
# s_full[2] = x[0]*w[2] + x[1]*w[1] + x[2]*w[0] = -1 + 0 + 3 = 2
# s_full[3] = x[1]*w[2] + x[2]*w[1] + x[3]*w[0] = -2 + 0 + 2 = 0
# s_full[4] = x[2]*w[2] + x[3]*w[1] + x[4]*w[0] = -3 + 0 + 1 = -2
# s_full[5] = x[3]*w[2] + x[4]*w[1] = -2 + 0 = -2
record('l6_toeplitz_conv_same', A_T @ x, s_same)

# Verify Lecture 6a c045 Toeplitz ordering explicitly:
# In c045, Lecture writes rows [w2, w3, 0, ...; w1, w2, w3, 0, ...], which corresponds to
# cross-correlation with [w1, w2, w3] (i.e. convolution with flipped kernel w_tilde = [w3, w2, w1]).
w_cc = np.array([1.0, 2.0, 3.0])
A_T_cc = np.array([
    [w_cc[1], w_cc[2], 0.,      0.,      0.],
    [w_cc[0], w_cc[1], w_cc[2], 0.,      0.],
    [0.,      w_cc[0], w_cc[1], w_cc[2], 0.],
    [0.,      0.,      w_cc[0], w_cc[1], w_cc[2]],
    [0.,      0.,      0.,      w_cc[0], w_cc[1]],
])
record('l6_toeplitz_crosscorr', A_T_cc @ x, np.correlate(x, w_cc, mode='same'))

# Translation equivariance check (with zero-padded shift)
x_a = np.array([0., 1., 2., 3., 0., 0., 0.])
x_shifted = np.array([0., 0., 1., 2., 3., 0., 0.])
record('l6_translation_equivariance',
       np.convolve(x_shifted, w, mode='same')[1:],
       np.convolve(x_a, w, mode='same')[:-1])


# 2. 2D Conv output shape & receptive field
def conv_out(h, k, p=0, s=1):
    return (h + 2 * p - k) // s + 1


# 2021B Q10 style 3-layer stack on 128x128 RGB
h1 = conv_out(128, 7, p=0, s=1)  # 122
h2 = conv_out(h1, 9, p=0, s=1)   # 114
h3 = conv_out(h2, 3, p=1, s=1)   # 114 ('same')
record('l6_3layer_feature_maps', [h1, h2, h3], [122, 114, 114])

# Receptive field recurrence: r_l = r_{l-1} + (k_l - 1) * J_{l-1}, J_l = J_{l-1} * s_l
def receptive_fields(layers):
    """layers: list of (kernel_size, stride)"""
    r, J = 1, 1
    out = []
    for k, s in layers:
        r = r + (k - 1) * J
        J = J * s
        out.append((r, J))
    return out


record('l6_rf_5_3_stride1', [r for r, _ in receptive_fields([(5, 1), (3, 1)])], [5, 7])
record('l6_rf_7_9_3_stride1', [r for r, _ in receptive_fields([(7, 1), (9, 1), (3, 1)])], [7, 15, 17])
record('l6_rf_mnist_deep_cnn', [r for r, _ in receptive_fields([(5, 2), (5, 2), (5, 1)])], [5, 13, 29])

# 3. Parameter counts (MNIST Shallow CNN, Deep CNN, and Dense vs Conv)
shallow_params = (
    10 * (1 * 5 * 5 + 1)        # conv1: 260
    + (10 * 14 * 14 + 1) * 50   # fc1: 98,050
    + (50 + 1) * 10             # fc2: 510
)
deep_params = (
    10 * (1 * 5 * 5 + 1)        # conv1: 260
    + 40 * (10 * 5 * 5 + 1)     # conv2: 10,040
    + 80 * (40 * 5 * 5 + 1)     # conv3: 80,080
    + (80 * 7 * 7 + 1) * 50     # fc1: 196,050
    + (50 + 1) * 10             # fc2: 510
)
record('l6_mnist_shallow_cnn_params', shallow_params, 98820)
record('l6_mnist_deep_cnn_params', deep_params, 286940)
record('l6_mnist_deep_shapes',
       [conv_out(28, 5, 2, 2), conv_out(14, 5, 2, 2), conv_out(7, 5, 2, 1)],
       [14, 7, 7])

# Dense vs Conv comparison for 32x32x3 -> 32x32x16, K=3
dense_32 = (3 * 32 * 32 + 1) * (16 * 32 * 32)
conv_32 = 16 * (3 * 3 * 3 + 1)
record('l6_dense_vs_conv_32', [dense_32, conv_32], [50348032, 448])

# 4. Regularization: L2 weight decay, ReLU scaling invariance, Bagging MSE, Dropout
w0, g0, eta, lam = 2.0, 0.5, 0.1, 0.2
w1 = (1.0 - eta * lam) * w0 - eta * g0
record('l6_weight_decay_step', w1, 1.91)

# ReLU positive homogeneity: (1/eps) A^T r(eps B^T x) == A^T r(B^T x)
B_mat = np.array([[1.0, -2.0], [0.5, 1.5]])
A_vec = np.array([2.0, -1.0])
x_in = np.array([1.2, 0.8])
eps = 10.0
f_orig = A_vec @ np.maximum(0.0, B_mat.T @ x_in)
f_scaled = (A_vec / eps) @ np.maximum(0.0, (eps * B_mat).T @ x_in)
record('l6_relu_rescaling_invariance', f_scaled, f_orig)
record('l6_relu_rescaling_A_norm_sq', [np.sum(A_vec ** 2), np.sum((A_vec / eps) ** 2)], [5.0, 0.05])

# Bagging MSE: MSE_c = V/K + (K-1)/K * C
V, K = 1.0, 5
mse_c_vals = [V / K + (K - 1) / K * C for C in (0.0, 0.5, 1.0)]
record('l6_bagging_mse', mse_c_vals, [0.2, 0.6, 1.0])

# Dropout expectation match (standard test-time scaling vs inverted dropout)
h_val, p_drop = 4.0, 0.5
record('l6_dropout_expectation', [(1.0 - p_drop) * h_val, (1.0 - p_drop) * (h_val / (1.0 - p_drop))], [2.0, 4.0])


# =============================================================================
# LECTURE 7 NUMERICAL VERIFICATIONS
# =============================================================================

# 1. Vanishing gradient chain & path counts
record('l7_sigmoid_chain', [0.25 ** 4, 0.25 ** 10], [0.00390625, 9.5367431640625e-07])
record('l7_path_counts', [10 ** 4, 3 ** 4], [10000, 81])

# 2. BatchNorm forward pass & bias cancellation
y_bn = np.array([2.0, 4.0, 6.0, 8.0])
mu = y_bn.mean()
var = y_bn.var()  # population variance over mini-batch = 5.0
y_hat = (y_bn - mu) / np.sqrt(var)  # eps -> 0 exact textbook check
gamma, beta = 2.0, 1.0
z_bn = gamma * y_hat + beta
record('l7_bn_mu_var', [mu, var], [5.0, 5.0])
record('l7_bn_yhat', y_hat, np.array([-3., -1., 1., 3.]) / np.sqrt(5.0))
record('l7_bn_z_stats', [z_bn.mean(), z_bn.var()], [beta, gamma ** 2])
# Bias cancellation: adding +100 to every y_i produces identical y_hat
y_bn_shifted = y_bn + 100.0
y_hat_shifted = (y_bn_shifted - y_bn_shifted.mean()) / np.sqrt(y_bn_shifted.var())
record('l7_bn_bias_cancellation', y_hat_shifted, y_hat)

# 3. Learning rate schedules (Lecture7a c036, c038, c047)
eta0, etaT, T = 0.02, 0.0001, 50
lr_lin_25 = (1.0 - 25 / T) * eta0 + (25 / T) * etaT
lr_dec_1000 = eta0 / (1.0 + 1e-3 * 1000)
record('l7_lr_schedules', [lr_lin_25, lr_dec_1000], [0.01005, 0.01])

# 4. Momentum vs Nesterov Momentum on L(w) = 0.5 * w^2 (grad = w)
# Lecture 7a convention: v^(t) = alpha * v^(t-1) - eta * grad, w^(t) = w^(t-1) + v^(t)
w_m, v_m = 4.0, 0.0
alpha_m, eta_m = 0.9, 0.1
hist_m = []
for _ in range(2):
    g = w_m
    v_m = alpha_m * v_m - eta_m * g
    w_m = w_m + v_m
    hist_m.append((v_m, w_m))
record('l7_momentum_2steps', [hist_m[0][0], hist_m[0][1], hist_m[1][0], hist_m[1][1]],
       [-0.4, 3.6, -0.72, 2.88])

w_n, v_n = 4.0, 0.0
hist_n = []
for _ in range(2):
    w_tilde = w_n + alpha_m * v_n
    g = w_tilde
    v_n = alpha_m * v_n - eta_m * g
    w_n = w_n + v_n
    hist_n.append((w_tilde, v_n, w_n))
# Step 1: w_tilde=4.0, v=-0.4, w=3.6
# Step 2: w_tilde=3.6+0.9*(-0.4)=3.24, v=0.9*(-0.4)-0.1*3.24=-0.684, w=3.6-0.684=2.916
record('l7_nesterov_2steps', [hist_n[1][0], hist_n[1][1], hist_n[1][2]], [3.24, -0.684, 2.916])

# 5. AdaGrad, RMSProp, Adam step-1 numerical check (g1 = 2.0, g2 = 2.0, w0 = 1.0, eta = 0.1, delta = 0 for clean algebra)
g1 = 2.0
eta_a = 0.1
# AdaGrad: r1 = 4, step = -0.1 * 2 / 2 = -0.1 -> w1 = 0.9; r2 = 8, step = -0.1 * 2 / sqrt(8)
r1_ada = g1 ** 2
w1_ada = 1.0 - eta_a / np.sqrt(r1_ada) * g1
r2_ada = r1_ada + g1 ** 2
w2_ada = w1_ada - eta_a / np.sqrt(r2_ada) * g1
record('l7_adagrad_2steps', [w1_ada, w2_ada], [0.9, 0.9 - 0.1 / np.sqrt(2.0)])

# RMSProp (rho=0.9): r1 = 0.1 * 4 = 0.4, w1 = 1 - 0.1 * 2 / sqrt(0.4)
r1_rms = 0.1 * g1 ** 2
w1_rms = 1.0 - eta_a / np.sqrt(r1_rms) * g1
record('l7_rmsprop_step1', [r1_rms, w1_rms], [0.4, 1.0 - 0.2 / np.sqrt(0.4)])

# Adam (rho1=0.9, rho2=0.999, delta=0 for exact step-1 insight):
rho1, rho2 = 0.9, 0.999
s1 = (1.0 - rho1) * g1          # 0.2
r1 = (1.0 - rho2) * (g1 ** 2)   # 0.004
s1_hat = s1 / (1.0 - rho1)      # 2.0
r1_hat = r1 / (1.0 - rho2)      # 4.0
w1_adam = 1.0 - eta_a * s1_hat / np.sqrt(r1_hat)  # 1.0 - 0.1 = 0.9
record('l7_adam_step1', [s1, r1, s1_hat, r1_hat, w1_adam], [0.2, 0.004, 2.0, 4.0, 0.9])

# 6. VGG 3x3 stacking vs 5x5 / 7x7 parameter ratio (unit C^2)
record('l7_vgg_param_ratios', [2 * 9 / 25, 3 * 9 / 49], [0.72, 27 / 49])

# 7. ResNet path counts: 2^N and C(N, L)
record('l7_resnet_paths_3', [math.comb(3, L) for L in range(4)], [1, 3, 3, 1])
record('l7_resnet_paths_10', 2 ** 10, 1024)

# 8. Scaled Dot-Product Attention (Lecture 7b column-vector convention!)
# d_k = 4, d_v = 2, n = 2 tokens
Q = np.array([[2., 0.], [0., 2.], [0., 0.], [0., 0.]])  # (4, 2)
K = np.array([[2., 0.], [0., 2.], [0., 0.], [0., 0.]])  # (4, 2)
V = np.array([[10., 0.], [0., 20.]])                    # (2, 2)
scores = (K.T @ Q) / np.sqrt(4.0)                       # [[2, 0], [0, 2]]
A_attn = softmax(scores, axis=0)                        # column-wise softmax!
out_attn = V @ A_attn
p_self = np.exp(2.0) / (np.exp(2.0) + 1.0)
p_other = 1.0 / (np.exp(2.0) + 1.0)
record('l7_attention_scores', scores, [[2., 0.], [0., 2.]])
record('l7_attention_weights', A_attn, [[p_self, p_other], [p_other, p_self]])
record('l7_attention_output', out_attn, [[10 * p_self, 10 * p_other], [20 * p_other, 20 * p_self]])

# Multi-Head & ViT dimensions
record('l7_mha_dims', [512 // 8, 224 // 16, (224 // 16) ** 2 + 1], [64, 14, 197])


# =============================================================================
# ORIGINAL TEACHING FIGURES (CLEAN, ENGLISH-LABELED, REPRODUCIBLE)
# =============================================================================

# Figure 1 (Lecture 6): Convolution modes, 2-layer receptive field & param comparison
fig, axs = plt.subplots(1, 2, figsize=(10.2, 3.7), gridspec_kw={'width_ratios': [1.15, 1.0]})

# Left panel: 2-layer receptive field stacking (|w1|=5, |w2|=3 -> RF=7)
ax = axs[0]
ax.set_xlim(-2.0, 8.7)
ax.set_ylim(-0.65, 2.85)
ax.set_aspect('equal', adjustable='box')
ax.axis('off')
ax.set_title('Receptive Field Stacking ($|w_1|=5,\\ |w_2|=3 \\Rightarrow \\mathrm{RF}=7$)', fontsize=10.2)

# Draw 9 input nodes (indices 0..8), highlight 1..7 (7 nodes in RF)
for i in range(9):
    active = 1 <= i <= 7
    fc = '#456b8d' if active else '#e5e9ec'
    ec = '#2c4863' if active else '#9aa5ad'
    tc = 'white' if active else '#555'
    ax.add_patch(plt.Circle((i, 0.25), 0.34, facecolor=fc, edgecolor=ec, lw=1.2, zorder=3))
    ax.text(i, 0.25, f'$x_{i}$', ha='center', va='center', fontsize=8.3, color=tc, zorder=4)

# Draw 3 layer-1 nodes at positions 3, 4, 5 (covering 1..5, 2..6, 3..7)
for pos in [3, 4, 5]:
    ax.add_patch(plt.Circle((pos, 1.35), 0.34, facecolor='#448775', edgecolor='#2d5f51', lw=1.2, zorder=3))
    ax.text(pos, 1.35, f'$h_{pos}$', ha='center', va='center', fontsize=8.3, color='white', zorder=4)
    for src in range(pos - 2, pos + 3):
        ax.plot([src, pos], [0.59, 1.01], color='#8aa89f', lw=1.0, alpha=0.8, zorder=1)

# Draw 1 layer-2 node at position 4 (covering h_3, h_4, h_5)
ax.add_patch(plt.Circle((4, 2.40), 0.35, facecolor='#a45b44', edgecolor='#733c2b', lw=1.3, zorder=3))
ax.text(4, 2.40, '$z_4$', ha='center', va='center', fontsize=8.8, color='white', zorder=4)
for pos in [3, 4, 5]:
    ax.plot([pos, 4], [1.69, 2.05], color='#a45b44', lw=1.5, zorder=2)

ax.annotate('', xy=(0.8, -0.25), xytext=(7.2, -0.25),
            arrowprops=dict(arrowstyle='<->', color='#2c4863', lw=1.4))
ax.text(4, -0.40, '7 input positions affect $z_4$', ha='center', va='top', fontsize=8.8, color='#2c4863')
ax.text(-1.85, 0.25, 'Input', ha='left', va='center', fontsize=8.5, color='#444')
ax.text(-1.85, 1.35, 'Conv1\n(K=5)', ha='left', va='center', fontsize=8.5, color='#2d5f51')
ax.text(-1.85, 2.40, 'Conv2\n(K=3)', ha='left', va='center', fontsize=8.5, color='#733c2b')

# Right panel: Parameter count (log scale) for 32x32x3 -> 32x32xF (K=3)
ax2 = axs[1]
F_vals = np.array([4, 8, 16, 32, 64])
dense_p = (3 * 32 * 32 + 1) * (F_vals * 32 * 32)
conv_p = F_vals * (3 * 3 * 3 + 1)
x_pos = np.arange(len(F_vals))
width = 0.36
ax2.bar(x_pos - width / 2, dense_p, width, label='Fully-connected (Dense)', color='#a45b44')
ax2.bar(x_pos + width / 2, conv_p, width, label='3x3 Conv2D (weight sharing)', color='#456b8d')
ax2.set_yscale('log')
ax2.set_ylim(40, 3e9)
ax2.set_xticks(x_pos)
ax2.set_xticklabels([f'F={f}' for f in F_vals])
ax2.set_ylabel('Parameter count (log scale)')
ax2.set_title('32x32x3 $\\rightarrow$ 32x32xF: Dense vs Conv', fontsize=10.2)
ax2.grid(axis='y', alpha=0.25)
ax2.legend(fontsize=8.3, loc='upper left')
for i in [2]:
    ax2.text(x_pos[i] - width / 2, dense_p[i] * 1.45, '50.3M', ha='center', fontsize=8.2, color='#733c2b')
    ax2.text(x_pos[i] + width / 2, conv_p[i] * 1.55, '448', ha='center', fontsize=8.2, color='#2c4863')
save(fig, 'l6-conv-receptive-field.png')


# Figure 2 (Lecture 6): Training vs Validation Loss Curve Diagnosis
ep = np.linspace(0, 50, 120)
fig, axs = plt.subplots(1, 3, figsize=(10.2, 3.1), sharey=False)

# (a) Overfitting
tr_a = 1.6 * np.exp(-ep / 9.0) + 0.05
va_a = 1.6 * np.exp(-ep / 8.0) + 0.25 + 0.0009 * np.maximum(ep - 14.0, 0) ** 2
axs[0].plot(ep, tr_a, color='#456b8d', lw=2, label='Training loss')
axs[0].plot(ep, va_a, '--', color='#a45b44', lw=2, label='Validation loss')
axs[0].axvline(15.5, color='#448775', ls=':', lw=1.5)
axs[0].text(16.8, 1.05, 'Early-stop\nzone', fontsize=8.5, color='#2d5f51')
axs[0].set_title('(a) Overfitting (Val rises)')
axs[0].set_xlabel('Epoch')
axs[0].set_ylabel('Loss')
axs[0].grid(alpha=0.2)
axs[0].legend(fontsize=8.2, loc='upper right')

# (b) Large generalization gap
tr_b = 1.5 * np.exp(-ep / 7.0) + 0.08
va_b = 1.3 * np.exp(-ep / 7.0) + 0.72
axs[1].plot(ep, tr_b, color='#456b8d', lw=2, label='Training loss')
axs[1].plot(ep, va_b, '--', color='#a45b44', lw=2, label='Validation loss')
axs[1].annotate('', xy=(38, 0.09), xytext=(38, 0.72),
                arrowprops=dict(arrowstyle='<->', color='#93764b', lw=1.4))
axs[1].text(39.5, 0.40, 'Wide\ngap', fontsize=8.5, color='#705834', va='center')
axs[1].set_title('(b) Large Generalization Gap')
axs[1].set_xlabel('Epoch')
axs[1].grid(alpha=0.2)

# (c) Under-converged
tr_c = 1.9 - 0.020 * ep
va_c = 2.0 - 0.019 * ep
axs[2].plot(ep, tr_c, color='#456b8d', lw=2, label='Training loss')
axs[2].plot(ep, va_c, '--', color='#a45b44', lw=2, label='Validation loss')
axs[2].set_title('(c) Under-converged (Still falling)')
axs[2].set_xlabel('Epoch')
axs[2].set_ylim(0.5, 2.2)
axs[2].grid(alpha=0.2)
save(fig, 'l6-loss-diagnosis.png')


# Figure 3 (Lecture 7): BatchNorm normalization + Optimizer trajectories on an elongated quadratic
fig, axs = plt.subplots(1, 2, figsize=(9.8, 3.6))

# Left panel: BatchNorm pulls drifted pre-activations back into active regime
u = np.linspace(-6, 10, 400)
p_raw = np.exp(-0.5 * ((u - 5.0) / 1.8) ** 2) / (1.8 * np.sqrt(2 * np.pi))
p_bn = np.exp(-0.5 * (u / 1.0) ** 2) / np.sqrt(2 * np.pi)
sig_prime = (1 / (1 + np.exp(-u))) * (1 - 1 / (1 + np.exp(-u)))
axs[0].fill_between(u, p_raw, color='#a45b44', alpha=0.28, label='Raw pre-activation $y$ (drifted)')
axs[0].plot(u, p_raw, color='#a45b44', lw=1.6)
axs[0].fill_between(u, p_bn, color='#456b8d', alpha=0.30, label='Normalized $\\hat{y}$ ($\\mu=0,\\sigma^2=1$)')
axs[0].plot(u, p_bn, color='#456b8d', lw=1.8)
axs[0].plot(u, sig_prime * 1.4, ':', color='#448775', lw=1.8, label='Active gradient zone (scaled)')
axs[0].set_title('BatchNorm Stabilizes Activation Scale')
axs[0].set_xlabel('Pre-activation value')
axs[0].set_ylabel('Density / Relative slope')
axs[0].grid(alpha=0.2)
axs[0].legend(fontsize=8.2, loc='upper right')

# Right panel: Elongated quadratic valley L(w1, w2) = 0.5*(w1^2 + 12*w2^2)
w1g, w2g = np.meshgrid(np.linspace(-2.2, 2.2, 120), np.linspace(-1.1, 1.1, 120))
Lg = 0.5 * (w1g ** 2 + 12.0 * w2g ** 2)
axs[1].contour(w1g, w2g, Lg, levels=[0.2, 0.6, 1.5, 3.0, 5.5], colors='#cccccc', linewidths=0.9)


def run_opt(mode, steps=22):
    w = np.array([-2.0, 0.85])
    v = np.zeros(2)
    s = np.zeros(2)
    r = np.zeros(2)
    pts = [w.copy()]
    for t in range(1, steps + 1):
        g = np.array([w[0], 12.0 * w[1]])
        if mode == 'gd':
            w = w - 0.14 * g
        elif mode == 'mom':
            v = 0.72 * v - 0.08 * g
            w = w + v
        elif mode == 'adam':
            s = 0.8 * s + 0.2 * g
            r = 0.95 * r + 0.05 * (g ** 2)
            sh = s / (1.0 - 0.8 ** t)
            rh = r / (1.0 - 0.95 ** t)
            w = w - 0.22 * sh / (1e-8 + np.sqrt(rh))
        pts.append(w.copy())
    return np.array(pts)


p_gd = run_opt('gd')
p_mom = run_opt('mom')
p_adam = run_opt('adam')
axs[1].plot(p_gd[:, 0], p_gd[:, 1], 'o-', ms=2.8, lw=1.4, color='#a45b44', label='Plain GD (zig-zag)')
axs[1].plot(p_mom[:, 0], p_mom[:, 1], 's-', ms=2.8, lw=1.7, color='#456b8d', label='Momentum (damps oscillation)')
axs[1].plot(p_adam[:, 0], p_adam[:, 1], '^-', ms=2.8, lw=1.7, color='#448775', label='Adam (per-coord scaling)')
axs[1].plot(0, 0, '*', ms=9, color='#222222')
axs[1].set_title('Optimization on Elongated Loss Valley')
axs[1].set_xlabel('$w_1$ (shallow curvature)')
axs[1].set_ylabel('$w_2$ (steep curvature)')
axs[1].set_xlim(-2.2, 0.8)
axs[1].set_ylim(-1.05, 1.05)
axs[1].legend(fontsize=8.0, loc='lower right')
save(fig, 'l7-bn-optimizers.png')


# Figure 4 (Lecture 7): ResNet path-length distribution vs gradient contribution + ViT vs ResNet inductive bias
fig, axs = plt.subplots(1, 2, figsize=(9.8, 3.6))

# Left panel: N=20 residual blocks — C(20, L) distribution vs decaying per-path gradient -> short-to-mid paths dominate
N_res = 20
Ls = np.arange(0, N_res + 1)
counts = np.array([math.comb(N_res, int(L)) for L in Ls], dtype=float)
count_share = counts / counts.sum()
# Illustrative exponential per-path gradient decay (gamma=0.6^L) to show total contribution = count * per_path
per_path_grad = 0.55 ** Ls
total_grad = counts * per_path_grad
total_grad_share = total_grad / total_grad.sum()

axs[0].bar(Ls - 0.18, count_share, width=0.36, color='#b6c6d4', label='Share of $2^{20}$ paths $\\binom{20}{L}/2^{20}$')
axs[0].bar(Ls + 0.18, total_grad_share, width=0.36, color='#456b8d', label='Illustrative total gradient share')
axs[0].set_title('ResNet ($N=20$): Short Paths Dominate', fontsize=10.2)
axs[0].set_xlabel('Path length $L$ (number of active blocks)')
axs[0].set_ylabel('Normalized share')
axs[0].grid(axis='y', alpha=0.2)
axs[0].legend(fontsize=8.1, loc='upper right')

# Right panel: Conceptual ViT vs ResNet data-scale trade-off (Lecture 7b c049-c050)
x_data = np.array([0, 1, 2])
labels_d = ['IN1k\n(1.3M)', 'IN21k\n(14M)', 'JFT\n(303M)']
# Qualitative schematic matching Lecture 7b c049: ViT < ResNet on IN1k, ~ on IN21k, > on JFT
resnet_rel = [81.5, 84.5, 86.0]
vit_rel = [77.5, 84.2, 88.5]
axs[1].plot(x_data, resnet_rel, 'o-', lw=2.0, color='#93764b', label='ResNet / CNN (strong inductive bias)')
axs[1].plot(x_data, vit_rel, 's-', lw=2.0, color='#448775', label='ViT (weak bias, scales with data)')
axs[1].set_xticks(x_data)
axs[1].set_xticklabels(labels_d)
axs[1].set_ylim(74, 91)
axs[1].set_ylabel('ImageNet-1k accuracy (schematic)')
axs[1].set_title('Inductive Bias vs Pre-training Scale', fontsize=10.2)
axs[1].grid(alpha=0.2)
axs[1].legend(fontsize=8.1, loc='lower right')
fig.subplots_adjust(wspace=0.28)
save(fig, 'l7-resnet-paths.png')

(D / 'l6-l7-example-results.json').write_text(json.dumps(checks, indent=2) + '\n')
print(f'All {len(checks)} checks passed and 4 figures generated.')
