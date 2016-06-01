"""
This configuration file loads environment's specific config settings for the application.
"""
import os

if "OPENSHIFT_PYTHON_DIR" in os.environ:
    from prod import config
else:
    from local import config
