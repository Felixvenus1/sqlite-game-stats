"""Shared pytest configuration.

Force matplotlib onto the headless Agg backend so the Pareto chart tests run
without a display (e.g. in CI).
"""

import matplotlib

matplotlib.use("Agg")
