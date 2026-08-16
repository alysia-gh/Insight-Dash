"""Compatibility shim: re-export from the capitalized package if present.

This project appears to contain an `Insights` directory (capital I).
Some environments may import `insights` (lowercase). To be robust,
re-export the capitalized package here when available.
"""
try:
	# If the project uses a capitalized `Insights` folder, re-export from it.
	import importlib
	pkg = importlib.import_module("Insights")
	for attr in dir(pkg):
		if not attr.startswith("__"):
			globals()[attr] = getattr(pkg, attr)
except Exception:
	# Nothing to do; keep this package minimal and let normal imports work.
	pass 

