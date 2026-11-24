"""Generate clean, original, reproducible diagrams for the CS5489 Final Exam Combined Q&A booklet."""
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(parents=True, exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.cache/matplotlib'))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.size': 10.0,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

rng = np.random.default_rng(2026)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(ASSETS / name, dpi=160, bbox_inches='tight')
    plt.close(fig)


# 1. 2020B Q8: Straight Voronoi (K-Means) vs Curved Mahalanobis (GMM) on 3 elongated vertical clusters
fig, axs = plt.subplots(1, 2, figsize=(8.8, 3.4))
mus = [np.array([-2.5, -2.0]), np.array([0.4, 1.0]), np.array([-1.0, -3.7])]
covs = [
    np.array([[0.35, -0.05], [-0.05, 1.1]]),
    np.array([[0.22, 0.02], [0.02, 1.4]]),
    np.array([[0.65, 0.2], [0.2, 1.1]]),
]
pis = [0.35, 0.35, 0.30]
cols_pt = ['#c94c4c', '#3c9d7e', '#6f42c1']
cols_bg = ['#f7d9d9', '#d7f2e8', '#e5daf7']
pts_list = [rng.multivariate_normal(m, c, size=38) for m, c in zip(mus, covs)]
xx, yy = np.meshgrid(np.linspace(-9.5, 6.5, 220), np.linspace(-8.5, 5.8, 220))
grid = np.c_[xx.ravel(), yy.ravel()]

# (a) K-Means Euclidean
dists = np.stack([np.sum((grid - m) ** 2, axis=1) for m in mus], axis=1)
Z_a = np.argmin(dists, axis=1).reshape(xx.shape)
axs[0].contourf(xx, yy, Z_a, levels=[-0.5, 0.5, 1.5, 2.5], colors=cols_bg, alpha=0.85)
for p, col, m in zip(pts_list, cols_pt, mus):
    axs[0].scatter(p[:, 0], p[:, 1], s=20, c=col, edgecolors='#222', lw=0.6)
    axs[0].scatter(m[0], m[1], s=140, marker='*', c=col, edgecolors='#111', lw=0.9, zorder=5)
axs[0].set_title('(a) Straight Boundaries (K-Means)')
axs[0].grid(alpha=0.25)

# (b) GMM Mahalanobis
def mvpdf(g, m, c):
    inv = np.linalg.inv(c)
    det = np.linalg.det(c)
    d = g - m
    return np.exp(-0.5 * np.sum((d @ inv) * d, axis=1)) / (2 * np.pi * np.sqrt(det))

probs = np.stack([pi * mvpdf(grid, m, c) for pi, m, c in zip(pis, mus, covs)], axis=1)
Z_b = np.argmax(probs, axis=1).reshape(xx.shape)
axs[1].contourf(xx, yy, Z_b, levels=[-0.5, 0.5, 1.5, 2.5], colors=cols_bg, alpha=0.85)
for p, col, m in zip(pts_list, cols_pt, mus):
    axs[1].scatter(p[:, 0], p[:, 1], s=20, c=col, edgecolors='#222', lw=0.6)
    axs[1].scatter(m[0], m[1], s=140, marker='*', c=col, edgecolors='#111', lw=0.9, zorder=5)
axs[1].set_title('(b) Curved Boundaries (GMM)')
axs[1].grid(alpha=0.25)
save(fig, 'final-2020b-q8.png')


# 2. 2020B Q9 & 2021B Q11: Three loss curve archetypes (a) Overfitting, (b) Large gap, (c) Under-converged
ep = np.linspace(0, 50, 120)
fig, axs = plt.subplots(1, 3, figsize=(9.6, 2.8))
curves = [
    ('(a) Overfitting', 1.6 * np.exp(-ep / 9) + 0.05, 1.6 * np.exp(-ep / 8) + 0.25 + 0.0009 * np.maximum(ep - 14, 0) ** 2),
    ('(b) Large Gap', 1.5 * np.exp(-ep / 7) + 0.08, 1.3 * np.exp(-ep / 7) + 0.72),
    ('(c) Still Converging', 1.9 - 0.022 * ep, 2.1 - 0.021 * ep),
]
for ax, (title, tr, va) in zip(axs, curves):
    ax.plot(ep, tr, color='#c94c4c', lw=2.0, label='Training loss')
    ax.plot(ep, va, color='#3a75a8', lw=2.0, label='Validation loss')
    ax.set_title(title, fontsize=9.8)
    ax.set_xlabel('Epoch')
    ax.set_yticks([])
    ax.set_xticks([])
    ax.grid(alpha=0.18)
axs[0].set_ylabel('Loss')
axs[0].legend(fontsize=8.0, loc='upper right')
save(fig, 'final-2020b-q9.png')


# 3. 2021B Q8: Dataset A (3 intersecting spokes) & Dataset B (3 stacked sine-wave manifolds)
fig, axs = plt.subplots(1, 2, figsize=(8.8, 3.5))
# Dataset A: 3 intersecting elongated Gaussians centered at origin at 0, 60, 120 deg
for ang_deg in [0, 60, 120]:
    ang = np.radians(ang_deg)
    R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    cov_s = R @ np.diag([12.0, 0.14]) @ R.T
    pts_s = rng.multivariate_normal([0, 0], cov_s, size=95)
    axs[0].scatter(pts_s[:, 0], pts_s[:, 1], s=14, c='#3a64a8', edgecolors='#111', lw=0.4)
axs[0].set_xlim(-9.5, 9.5)
axs[0].set_ylim(-9.5, 9.5)
axs[0].set_aspect('equal')
axs[0].set_title('(a) Dataset A: 3 Intersecting Spokes')
axs[0].grid(alpha=0.25)

# Dataset B: 3 parallel sinusoidal manifolds
for y_off in [-4.0, 0.0, 4.0]:
    xs = rng.uniform(-5.0, 5.0, size=220)
    ys = y_off + 2.0 * np.cos(1.5 * xs) + rng.normal(0, 0.25, size=220)
    axs[1].scatter(xs, ys, s=14, c='#3a64a8', edgecolors='#111', lw=0.4)
axs[1].set_xlim(-7.0, 7.0)
axs[1].set_ylim(-7.5, 7.5)
axs[1].set_title('(b) Dataset B: 3 Wave Manifolds')
axs[1].grid(alpha=0.25)
save(fig, 'final-2021b-q8.png')


# 4. 2021B Q9: Sigmoid vs Piecewise-Linear hard-sigmoid phi(z) on [-4, 4]
fig, ax = plt.subplots(figsize=(6.2, 3.0))
z = np.linspace(-10, 10, 400)
sig = 1.0 / (1.0 + np.exp(-z))
pwl = np.clip((z + 4.0) / 8.0, 0.0, 1.0)
ax.plot(z, sig, color='#c94c4c', lw=2.0, label='Sigmoid $\\sigma(z)$')
ax.plot(z, pwl, color='#2c5d9e', lw=2.2, label='Piecewise linear $\\phi(z)$')
ax.axvline(-4, color='#777', ls=':', lw=1.0)
ax.axvline(4, color='#777', ls=':', lw=1.0)
ax.set_xlabel('$z = f(x)$')
ax.set_ylabel('Output probability')
ax.set_title('2021B Q9: Sigmoid vs Piecewise-Linear Activation $\\phi(z)$')
ax.grid(alpha=0.22)
ax.legend(fontsize=8.8, loc='upper left')
save(fig, 'final-2021b-q9.png')


# 5. 2021A Q11(b): Gradient noise distribution — Adam (lighter tail) vs SGD (longer heavy tail)
fig, axs = plt.subplots(1, 2, figsize=(8.8, 3.1), sharey=True)
noise_adam = rng.exponential(scale=32.0, size=18000)
noise_sgd = rng.lognormal(mean=3.0, sigma=1.05, size=18000)
noise_sgd = noise_sgd[noise_sgd < 890]
bins = np.linspace(0, 900, 120)
axs[0].hist(noise_adam, bins=bins, color='#6ca0cc', alpha=0.85)
axs[0].set_yscale('log')
axs[0].set_xlim(0, 900)
axs[0].set_xticks([0, 450, 900])
axs[0].set_title('Adam (Shorter / Lighter Tail)')
axs[0].set_xlabel('Gradient noise magnitude (illustrative)')
axs[0].set_ylabel('Count (log scale)')
axs[0].grid(alpha=0.2)

axs[1].hist(noise_sgd, bins=bins, color='#456b8d', alpha=0.85)
axs[1].set_yscale('log')
axs[1].set_xlim(0, 900)
axs[1].set_xticks([0, 450, 900])
axs[1].set_title('SGD (Longer Heavy Tail)')
axs[1].set_xlabel('Gradient noise magnitude (illustrative)')
axs[1].grid(alpha=0.2)
save(fig, 'final-2021a-q11.png')

print('Generated all 5 clean original figures for CS5489 Final Combined Q&A.')
