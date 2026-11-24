"""Deterministic numerical checks and original teaching figures for CS5489 Lectures 8 and 9."""
from pathlib import Path
import json
import os

D = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(D / '.cache/matplotlib'))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

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
# LECTURE 8 NUMERICAL VERIFICATIONS
# =============================================================================

# 1. Exact 2D PCA worked example: variance maximization == reconstruction error minimization
X_pca = np.array([[-2., -1.], [-1., -2.], [1., 2.], [2., 1.]])
mu_pca = X_pca.mean(axis=0)
Sigma_pca = (X_pca.T @ X_pca) / len(X_pca)  # population covariance matching Lecture 8a c020
eigvals, eigvecs = np.linalg.eigh(Sigma_pca)
order = np.argsort(eigvals)[::-1]
eigvals = eigvals[order]
eigvecs = eigvecs[:, order]
# Canonicalize sign of v1 = [1, 1]/sqrt(2)
if eigvecs[0, 0] < 0:
    eigvecs[:, 0] *= -1
v1 = eigvecs[:, 0]
w_proj = X_pca @ v1
X_hat = np.outer(w_proj, v1)
preserved_var = np.mean(w_proj ** 2)
recon_mse = np.mean(np.sum((X_pca - X_hat) ** 2, axis=1))
record('l8_pca_mean', mu_pca, [0., 0.])
record('l8_pca_cov', Sigma_pca, [[2.5, 2.0], [2.0, 2.5]])
record('l8_pca_eigvals', eigvals, [4.5, 0.5])
record('l8_pca_v1', v1, [1. / np.sqrt(2.), 1. / np.sqrt(2.)])
record('l8_pca_var_recon_identity', [preserved_var, recon_mse, preserved_var + recon_mse], [4.5, 0.5, 5.0])
record('l8_pca_explained_ratio', eigvals[0] / eigvals.sum(), 0.9)

# 2. PCA vs FLD (LDA) on 2 parallel elongated classes
mu1_fld = np.array([0., 1.])
mu2_fld = np.array([0., -1.])
S1_fld = np.diag([10., 0.2])
S2_fld = np.diag([10., 0.2])
w_fld = np.linalg.solve(S1_fld + S2_fld, mu1_fld - mu2_fld)
record('l8_fld_direction', w_fld, [0., 5.])
# Fisher criterion J(w) along [0, 1] vs [1, 0]
def fisher_j(w):
    num = (w @ (mu1_fld - mu2_fld)) ** 2
    den = w @ (S1_fld + S2_fld) @ w
    return num / den
record('l8_fld_vs_pca_score', [fisher_j(np.array([0., 1.])), fisher_j(np.array([1., 0.]))], [10.0, 0.0])

# 3. PCA vs Linear-Kernel KPCA for N=1000, D=1,000,000 (2021B Final Q7)
N_big, D_big = 1000, 1_000_000
cov_bytes_tb = (D_big * D_big * 8) / 1e12   # 8 TB (decimal TB)
gram_bytes_mb = (N_big * N_big * 8) / 1e6   # 8 MB (decimal MB)
record('l8_pca_vs_kpca_memory', [cov_bytes_tb, gram_bytes_mb], [8.0, 8.0])
record('l8_pca_vs_kpca_flops_ratio', (N_big * D_big * D_big) / (N_big * N_big * D_big), 1000.0)

# 4. Kernel centering & linear KPCA equivalence to standard PCA
X_k = np.array([[1., 2.], [2., 1.], [4., 5.], [5., 4.]])
Xc = X_k - X_k.mean(axis=0)
K_lin = X_k @ X_k.T
H_c = np.eye(4) - np.ones((4, 4)) / 4.0
K_tilde = H_c @ K_lin @ H_c
eig_k, vec_k = np.linalg.eigh(K_tilde)
eig_k = eig_k[::-1]
vec_k = vec_k[:, ::-1]
# Top-1 KPCA score: a_1 = u_1 / sqrt(lam_1), score = K_tilde @ a_1 = sqrt(lam_1) * u_1
kpca_scores_abs = np.abs(K_tilde @ (vec_k[:, 0] / np.sqrt(eig_k[0])))
cov_k = (Xc.T @ Xc) / 4.0
eig_p, vec_p = np.linalg.eigh(cov_k)
pca_scores_abs = np.abs(Xc @ vec_p[:, -1])
record('l8_linear_kpca_matches_pca_eigval', eig_k[0] / 4.0, eig_p[-1])
record('l8_linear_kpca_matches_pca_scores', kpca_scores_abs, pca_scores_abs)

# 5. Geodesic vs Euclidean distance on a 3-point bent arc: (0,0) -> (1,0) -> (1,1)
p0, p1, p2 = np.array([0., 0.]), np.array([1., 0.]), np.array([1., 1.])
d_euclid = np.linalg.norm(p2 - p0)
d_geod = np.linalg.norm(p1 - p0) + np.linalg.norm(p2 - p1)
record('l8_geodesic_vs_euclid', [d_euclid, d_geod], [np.sqrt(2.0), 2.0])


# =============================================================================
# LECTURE 9 NUMERICAL VERIFICATIONS
# =============================================================================

# 1. K-Means 1D step-by-step worked example on {1, 2, 4, 5}, init c1=1, c2=2
pts_km = np.array([1., 2., 4., 5.])
c1, c2 = 1.0, 2.0
# Iter 1: assign
z1 = np.where(np.abs(pts_km - c1) <= np.abs(pts_km - c2), 1, 2)
c1_1, c2_1 = pts_km[z1 == 1].mean(), pts_km[z1 == 2].mean()
# Iter 2: assign
z2 = np.where(np.abs(pts_km - c1_1) <= np.abs(pts_km - c2_1), 1, 2)
c1_2, c2_2 = pts_km[z2 == 1].mean(), pts_km[z2 == 2].mean()
# Iter 3: assign unchanged
z3 = np.where(np.abs(pts_km - c1_2) <= np.abs(pts_km - c2_2), 1, 2)
sse_final = np.sum((pts_km - np.where(z3 == 1, c1_2, c2_2)) ** 2)
record('l9_kmeans_iter1_centers', [c1_1, c2_1], [1.0, 11.0 / 3.0])
record('l9_kmeans_final_centers', [c1_2, c2_2], [1.5, 4.5])
record('l9_kmeans_converged_assignments', z3, [1, 1, 2, 2])
record('l9_kmeans_final_sse', sse_final, 1.0)

# 2. 1D GMM E-step & M-step worked example on symmetric {0, 2, 4}
pts_gmm = np.array([0., 2., 4.])
pi1, pi2 = 0.5, 0.5
mu1, mu2 = 0.0, 4.0
var1, var2 = 2.0, 2.0

def gauss1d(x, mu, var):
    return np.exp(-0.5 * ((x - mu) ** 2) / var) / np.sqrt(2.0 * np.pi * var)

p1 = pi1 * gauss1d(pts_gmm, mu1, var1)
p2 = pi2 * gauss1d(pts_gmm, mu2, var2)
r1 = p1 / (p1 + p2)
r2 = p2 / (p1 + p2)
N1, N2 = r1.sum(), r2.sum()
mu1_new = (r1 @ pts_gmm) / N1
mu2_new = (r2 @ pts_gmm) / N2
var1_new = (r1 @ ((pts_gmm - mu1_new) ** 2)) / N1
var2_new = (r2 @ ((pts_gmm - mu2_new) ** 2)) / N2
p_end = 1.0 / (1.0 + np.exp(-4.0))
record('l9_gmm_r1_exact', r1, [p_end, 0.5, 1.0 - p_end])
record('l9_gmm_soft_counts', [N1, N2], [1.5, 1.5])
mu1_exp = (2.0 * 0.5 + 4.0 * (1.0 - p_end)) / 1.5
record('l9_gmm_mstep_means', [mu1_new, mu2_new], [mu1_exp, 4.0 - mu1_exp])
record('l9_gmm_mstep_vars', [var1_new, var2_new], [var1_new, var1_new])
print(f"GMM example: p_end={p_end:.4f}, mu1_new={mu1_new:.4f}, mu2_new={mu2_new:.4f}, var_new={var1_new:.4f}")

# 3. Same cluster centers, different assignments between K-Means and GMM (2021A Q7)
# Case A: Distinct centers mu1=0, mu2=4, equal priors, var1=0.25, var2=16
# Point x=1.5 is closer to mu1=0 (|1.5-0|=1.5 < |1.5-4|=2.5 -> K-Means picks cluster 1)
# Yet N(1.5 | 0, 0.25) = 0.00886 < N(1.5 | 4, 16) = 0.0821 -> GMM assigns to cluster 2!
p_c1 = 0.5 * gauss1d(1.5, 0.0, 0.25)
p_c2 = 0.5 * gauss1d(1.5, 4.0, 16.0)
post_c2 = p_c2 / (p_c1 + p_c2)
assert post_c2 > 0.90  # ~0.903!
# Case B: Identical centers mu1=mu2=0, var1=1, var2=16:
# x=0 -> N(0|0,1)=0.3989 > N(0|0,16)=0.0997 -> cluster 1; x=3 -> N(3|0,1)=0.00443 < N(3|0,16)=0.0753 -> cluster 2!
post_same_x0 = gauss1d(0.0, 0.0, 1.0) / (gauss1d(0.0, 0.0, 1.0) + gauss1d(0.0, 0.0, 16.0))
post_same_x3 = gauss1d(3.0, 0.0, 1.0) / (gauss1d(3.0, 0.0, 1.0) + gauss1d(3.0, 0.0, 16.0))
record('l9_same_center_diff_assign', [post_c2, post_same_x0, post_same_x3],
       [post_c2, 0.8, post_same_x3])
assert post_same_x0 == 0.8 and post_same_x3 < 0.06

# 4. Bayesian GMM Dirichlet weight smoothing: pi_j = (N_j + alpha)/(N + K*alpha)
N_tot, K_bg = 100.0, 5
Nj_arr = np.array([60., 40., 0., 0., 0.])
pi_small_alpha = (Nj_arr + 0.01) / (N_tot + K_bg * 0.01)
pi_large_alpha = (Nj_arr + 100.0) / (N_tot + K_bg * 100.0)
record('l9_bgmm_small_alpha_empty', pi_small_alpha[2], 0.01 / 100.05)
record('l9_bgmm_large_alpha_empty', pi_large_alpha[2], 100.0 / 600.0)

# 5. Spectral clustering Graph Laplacian L = D - A (4-node barbell graph)
A_gr = np.array([
    [0., 1., 0., 0.],
    [1., 0., 0.1, 0.],
    [0., 0.1, 0., 1.],
    [0., 0., 1., 0.],
])
D_gr = np.diag(A_gr.sum(axis=1))
L_gr = D_gr - A_gr
evals_L, evecs_L = np.linalg.eigh(L_gr)
fiedler = evecs_L[:, 1]
if fiedler[0] > 0:
    fiedler = -fiedler
# Signs should cleanly separate {0,1} (negative) from {2,3} (positive)
record('l9_laplacian_zero_eig', evals_L[0], 0.0)
record('l9_laplacian_fiedler_signs', np.sign(fiedler), [-1., -1., 1., 1.])
# Verify quadratic form y^T L y = 0.5 * sum_{i,j} A_{ij} (y_i - y_j)^2
y_test = np.array([1., 1., -1., -1.])
q_mat = float(y_test @ L_gr @ y_test)
q_sum = 0.5 * float(np.sum(A_gr * (y_test[:, None] - y_test[None, :]) ** 2))
record('l9_laplacian_quadform', [q_mat, q_sum], [0.4, 0.4])


# =============================================================================
# ORIGINAL TEACHING FIGURES (CLEAN, ENGLISH-LABELED, REPRODUCIBLE)
# =============================================================================

rng = np.random.default_rng(5489)

# Figure 1 (Lecture 8): PCA variance vs FLD class separation
fig, axs = plt.subplots(1, 2, figsize=(9.8, 3.6))

# Left: 2D PCA ellipse & orthogonal projection onto v1
ax = axs[0]
pts = rng.multivariate_normal([0, 0], [[2.5, 2.0], [2.0, 2.5]], size=90)
ax.scatter(pts[:, 0], pts[:, 1], s=18, color='#456b8d', alpha=0.65, label='Data points')
# Project 6 sample points orthogonally onto v1
sample_idx = [2, 11, 23, 37, 52, 74]
for idx in sample_idx:
    p = pts[idx]
    proj = (p @ v1) * v1
    ax.plot([p[0], proj[0]], [p[1], proj[1]], ':', color='#a45b44', lw=1.2)
    ax.plot(proj[0], proj[1], 'o', ms=3.5, color='#a45b44')
t_line = np.linspace(-4.2, 4.2, 50)
ax.plot(t_line * v1[0], t_line * v1[1], color='#2c4863', lw=2.0, label='1st PC $\\mathbf{v}_1$ (max var)')
ax.annotate('', xy=2.3 * v1, xytext=(0, 0), arrowprops=dict(arrowstyle='->', lw=2.2, color='#a45b44'))
ax.annotate('', xy=1.1 * eigvecs[:, 1], xytext=(0, 0), arrowprops=dict(arrowstyle='->', lw=1.8, color='#448775'))
ax.text(2.3 * v1[0] + 0.15, 2.3 * v1[1] - 0.35, '$\\mathbf{v}_1\\ (\\sqrt{\\lambda_1})$', fontsize=9, color='#a45b44')
ax.text(1.1 * eigvecs[0, 1] - 1.3, 1.1 * eigvecs[1, 1] + 0.2, '$\\mathbf{v}_2\\ (\\sqrt{\\lambda_2})$', fontsize=9, color='#2d5f51')
ax.set_aspect('equal')
ax.set_xlim(-4.5, 4.5)
ax.set_ylim(-4.0, 4.0)
ax.set_title('PCA: Max Variance = Min Orthogonal Error', fontsize=10.0)
ax.set_xlabel('$x_1$')
ax.set_ylabel('$x_2$')
ax.grid(alpha=0.2)
ax.legend(fontsize=8.2, loc='lower right')

# Right: Parallel elongated classes where PCA fails and FLD succeeds
ax2 = axs[1]
cA = rng.multivariate_normal([0, 1.25], [[4.5, 0.], [0., 0.12]], size=60)
cB = rng.multivariate_normal([0, -1.25], [[4.5, 0.], [0., 0.12]], size=60)
ax2.scatter(cA[:, 0], cA[:, 1], s=18, color='#456b8d', alpha=0.75, label='Class 1')
ax2.scatter(cB[:, 0], cB[:, 1], s=18, color='#a45b44', alpha=0.75, marker='^', label='Class 2')
ax2.axhline(0, color='#93764b', ls='--', lw=1.8, label='PCA $\\mathbf{v}_1$ (collapses classes!)')
ax2.axvline(0, color='#448775', ls='-', lw=2.0, label='FLD $\\mathbf{w}^*$ (separates classes)')
ax2.set_xlim(-6.2, 6.2)
ax2.set_ylim(-3.1, 3.1)
ax2.set_title('Unsupervised PCA vs Supervised FLD', fontsize=10.0)
ax2.set_xlabel('$x_1$ (high-variance noise)')
ax2.set_ylabel('$x_2$ (class signal)')
ax2.grid(alpha=0.2)
ax2.legend(fontsize=8.0, loc='lower right')
save(fig, 'l8-pca-vs-fld.png')


# Figure 2 (Lecture 8): Manifold geodesic (MDS vs Isomap) + Non-linear KPCA rings
fig, axs = plt.subplots(1, 2, figsize=(9.8, 3.6))

# Left: Bent 1D spiral manifold illustrating Euclidean vs Geodesic distance
ax = axs[0]
theta = np.linspace(0.4, 2.75 * np.pi, 180)
r_s = 0.25 + 0.18 * theta
xs = r_s * np.cos(theta)
ys = r_s * np.sin(theta)
ax.scatter(xs, ys, c=theta, cmap='viridis', s=14, alpha=0.85)
i_start, i_end = 18, 128
ax.plot([xs[i_start], xs[i_end]], [ys[i_start], ys[i_end]], '--', color='#a45b44', lw=2.2,
        label='Euclidean distance (MDS)')
ax.plot(xs[i_start:i_end + 1], ys[i_start:i_end + 1], '-', color='#2c4863', lw=2.5,
        label='Geodesic along manifold (Isomap)')
ax.scatter([xs[i_start], xs[i_end]], [ys[i_start], ys[i_end]], s=55, color='#a45b44', zorder=5)
ax.set_aspect('equal')
ax.set_title('Manifold: Euclidean vs Geodesic Distance', fontsize=10.0)
ax.set_xlabel('$x_1$')
ax.set_ylabel('$x_2$')
ax.grid(alpha=0.2)
ax.legend(fontsize=8.1, loc='lower left')

# Right: Concentric rings (linear PCA cannot separate; RBF KPCA 1st PC separates cleanly)
ax2 = axs[1]
ang1 = rng.uniform(0, 2 * np.pi, 70)
ang2 = rng.uniform(0, 2 * np.pi, 90)
r1 = 0.55 + rng.normal(0, 0.07, 70)
r2 = 1.45 + rng.normal(0, 0.08, 90)
ax2.scatter(r1 * np.cos(ang1), r1 * np.sin(ang1), s=18, color='#456b8d', label='Inner cluster (KPCA PC1 > 0)')
ax2.scatter(r2 * np.cos(ang2), r2 * np.sin(ang2), s=18, color='#a45b44', marker='^', label='Outer ring (KPCA PC1 < 0)')
# Draw a circular RBF iso-contour separating them
circ_t = np.linspace(0, 2 * np.pi, 100)
ax2.plot(1.0 * np.cos(circ_t), 1.0 * np.sin(circ_t), '--', color='#448775', lw=1.8, label='RBF KPCA nonlinear contour')
ax2.set_aspect('equal')
ax2.set_xlim(-2.0, 2.0)
ax2.set_ylim(-2.0, 2.0)
ax2.set_title('Non-linear Structure: Linear PCA vs RBF KPCA', fontsize=10.0)
ax2.set_xlabel('$x_1$')
ax2.set_ylabel('$x_2$')
ax2.grid(alpha=0.2)
ax2.legend(fontsize=7.8, loc='lower right')
save(fig, 'l8-manifold-geodesic.png')


# Figure 3 (Lecture 9): K-Means linear boundaries vs GMM elliptical/curved boundaries
fig, axs = plt.subplots(1, 2, figsize=(9.8, 3.6))

# Generate 2 skewed overlapping elliptical clusters
mu_a, cov_a = np.array([-0.7, 0.0]), np.array([[0.18, 0.0], [0.0, 2.4]])
mu_b, cov_b = np.array([1.1, 0.0]), np.array([[1.8, 0.7], [0.7, 0.45]])
Xa = rng.multivariate_normal(mu_a, cov_a, size=85)
Xb = rng.multivariate_normal(mu_b, cov_b, size=85)
X_all = np.vstack([Xa, Xb])

xx, yy = np.meshgrid(np.linspace(-3.0, 4.2, 200), np.linspace(-4.2, 4.2, 200))
grid = np.c_[xx.ravel(), yy.ravel()]

# Left: K-Means linear perpendicular bisector between true centers
d_km_a = np.sum((grid - mu_a) ** 2, axis=1)
d_km_b = np.sum((grid - mu_b) ** 2, axis=1)
Z_km = (d_km_b < d_km_a).reshape(xx.shape)
axs[0].contourf(xx, yy, Z_km, levels=[-0.5, 0.5, 1.5], colors=['#dce7f0', '#f4dfd8'], alpha=0.55)
axs[0].contour(xx, yy, Z_km, levels=[0.5], colors=['#333333'], linewidths=1.5, linestyles='--')
axs[0].scatter(Xa[:, 0], Xa[:, 1], s=16, color='#456b8d', alpha=0.8)
axs[0].scatter(Xb[:, 0], Xb[:, 1], s=16, color='#a45b44', marker='^', alpha=0.8)
axs[0].scatter([mu_a[0], mu_b[0]], [mu_a[1], mu_b[1]], s=80, c='#111111', marker='x', lw=2.2)
axs[0].set_title('K-Means: Straight Euclidean Boundary', fontsize=10.0)
axs[0].set_xlabel('$x_1$')
axs[0].set_ylabel('$x_2$')
axs[0].grid(alpha=0.2)

# Right: GMM curved Mahalanobis decision boundary + 1.5-sigma ellipses
def mvnorm_pdf(pts_g, mu, cov):
    inv = np.linalg.inv(cov)
    det = np.linalg.det(cov)
    diff = pts_g - mu
    quad = np.sum((diff @ inv) * diff, axis=1)
    return np.exp(-0.5 * quad) / (2.0 * np.pi * np.sqrt(det))

pa = 0.5 * mvnorm_pdf(grid, mu_a, cov_a)
pb = 0.5 * mvnorm_pdf(grid, mu_b, cov_b)
Z_gmm = (pb > pa).reshape(xx.shape)
axs[1].contourf(xx, yy, Z_gmm, levels=[-0.5, 0.5, 1.5], colors=['#dce7f0', '#f4dfd8'], alpha=0.55)
axs[1].contour(xx, yy, Z_gmm, levels=[0.5], colors=['#333333'], linewidths=1.5, linestyles='-')
axs[1].scatter(Xa[:, 0], Xa[:, 1], s=16, color='#456b8d', alpha=0.8)
axs[1].scatter(Xb[:, 0], Xb[:, 1], s=16, color='#a45b44', marker='^', alpha=0.8)
for mu, cov, col in [(mu_a, cov_a, '#2c4863'), (mu_b, cov_b, '#733c2b')]:
    vals, vecs = np.linalg.eigh(cov)
    ang = np.degrees(np.arctan2(vecs[1, 1], vecs[0, 1]))
    ell = Ellipse(mu, 3.2 * np.sqrt(vals[1]), 3.2 * np.sqrt(vals[0]), angle=ang,
                  fill=False, edgecolor=col, lw=1.6, ls=':')
    axs[1].add_patch(ell)
axs[1].set_title('GMM: Curved Mahalanobis Boundary', fontsize=10.0)
axs[1].set_xlabel('$x_1$')
axs[1].set_ylabel('$x_2$')
axs[1].grid(alpha=0.2)
save(fig, 'l9-kmeans-vs-gmm.png')


# Figure 4 (Lecture 9): 1D KDE + Mean-Shift mode climbing & Spectral Clustering on non-compact moons/rings
fig, axs = plt.subplots(1, 2, figsize=(9.8, 3.6))

# Left: 1D KDE density & Mean-Shift mode seeking
ax = axs[0]
samples_1d = np.array([-2.3, -1.9, -1.5, -1.2, 1.4, 1.8, 2.1, 2.5, 2.8])
x_grid = np.linspace(-4.5, 5.2, 400)
bw = 0.75
kernels = np.array([gauss1d(x_grid, s, bw ** 2) for s in samples_1d])
kde = kernels.mean(axis=0)
for k in kernels:
    ax.plot(x_grid, k / len(samples_1d), color='#b6c6d4', lw=0.9, ls='--')
ax.plot(x_grid, kde, color='#456b8d', lw=2.3, label='KDE $p(x)$ ($\\sigma=0.75$)')
ax.scatter(samples_1d, np.zeros_like(samples_1d) + 0.004, s=26, color='#222222', zorder=5, label='Data points $x_i$')
# Find 2 modes on left and right
left_mode = x_grid[np.argmax(kde[x_grid < 0])]
right_mask = x_grid > 0
right_mode = x_grid[right_mask][np.argmax(kde[right_mask])]
ax.scatter([left_mode, right_mode], [kde[x_grid == left_mode][0], kde[x_grid == right_mode][0]],
           s=65, color='#a45b44', zorder=6, label='Modes (cluster centers)')
# Draw mean-shift climbing arrows
ax.annotate('', xy=(left_mode - 0.1, kde[x_grid == left_mode][0] - 0.005),
            xytext=(-3.2, 0.045), arrowprops=dict(arrowstyle='->', lw=1.6, color='#448775'))
ax.annotate('', xy=(right_mode + 0.1, kde[x_grid == right_mode][0] - 0.005),
            xytext=(3.7, 0.055), arrowprops=dict(arrowstyle='->', lw=1.6, color='#448775'))
ax.text(-4.35, 0.125, 'Mean-shift\nclimbs density', fontsize=8.2, color='#2d5f51',
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.85, pad=1.5))
ax.set_ylim(-0.008, 0.305)
ax.set_title('KDE & Mean-Shift Mode Seeking', fontsize=10.0)
ax.set_xlabel('$x$')
ax.set_ylabel('Estimated density $p(x)$')
ax.grid(alpha=0.2)
ax.legend(fontsize=7.9, loc='upper left')

# Right: Non-compact two-moons manifold (connected graphs -> Spectral Clustering succeeds)
ax2 = axs[1]
t_m = np.linspace(0, np.pi, 65)
m1 = np.c_[np.cos(t_m), np.sin(t_m)] + rng.normal(0, 0.06, (65, 2))
m2 = np.c_[1.0 - np.cos(t_m), 0.45 - np.sin(t_m)] + rng.normal(0, 0.06, (65, 2))
# Draw local k-NN graph edges within each moon to illustrate connected components
for pts_m, col, lbl, mk in [(m1, '#456b8d', 'Manifold cluster 1', 'o'),
                             (m2, '#a45b44', 'Manifold cluster 2', '^')]:
    for i in range(len(pts_m) - 1):
        ax2.plot([pts_m[i, 0], pts_m[i + 1, 0]], [pts_m[i, 1], pts_m[i + 1, 1]],
                 color=col, alpha=0.28, lw=0.9)
    ax2.scatter(pts_m[:, 0], pts_m[:, 1], s=18, color=col, marker=mk, label=lbl, zorder=4)
ax2.set_title('Non-compact Manifolds: Spectral Clustering', fontsize=10.0)
ax2.set_xlabel('$x_1$')
ax2.set_ylabel('$x_2$')
ax2.grid(alpha=0.2)
ax2.legend(fontsize=8.1, loc='lower left')
save(fig, 'l9-meanshift-spectral.png')

(D / 'l8-l9-example-results.json').write_text(json.dumps(checks, indent=2) + '\n')
print(f'All {len(checks)} checks passed and 4 figures generated.')
