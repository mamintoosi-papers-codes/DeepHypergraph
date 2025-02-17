import pytest
import numpy as np
from pathlib import Path

import dhg.visualization as vis


@pytest.fixture()
def emb1():
    return np.random.rand(100, 32)


def test_draw_in_euclidean_space(emb1):
    tmp_path = Path("tmp/")
    if not tmp_path.exists():
        tmp_path.mkdir()
    fig = vis.draw_in_euclidean_space(emb1)
    fig.savefig(tmp_path / "test_draw_in_euclidean_space.png")
    fig = vis.draw_in_euclidean_space(emb1, dim=3)
    fig.savefig(tmp_path / "test_draw_in_euclidean_space_3d.png")


def test_draw_poincare_ball(emb1):
    tmp_path = Path("tmp/")
    if not tmp_path.exists():
        tmp_path.mkdir()
    fig = vis.draw_in_poincare_ball(emb1)
    fig.savefig(tmp_path / "test_draw_poincare_ball.png")
    fig = vis.draw_in_poincare_ball(emb1, dim=3)
    fig.savefig(tmp_path / "test_draw_poincare_ball_3d.png")
