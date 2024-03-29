#    Copyright 2017 - 2022 Alexey Stepanov aka penguinolog
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at

#         http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Advanced descriptors for special cases."""

# Local Implementation
from .advanced_property import AdvancedProperty
from .log_on_access import LogOnAccess
from .separate_class_method import SeparateClassMethod

__all__ = ("SeparateClassMethod", "AdvancedProperty", "LogOnAccess")

try:
    # Local Implementation
    from ._version import version as __version__
except ImportError:
    pass

__author__ = "Alexey Stepanov"
__author_email__ = "penguinolog@gmail.com"
__maintainers__ = {
    "Alexey Stepanov": "penguinolog@gmail.com",
    "Antonio Esposito": "esposito.cloud@gmail.com",
    "Dennis Dmitriev": "dis-xcom@gmail.com",
}
__url__ = "https://github.com/python-useful-helpers/advanced-descriptors"
__description__ = "Advanced descriptors for special cases."
__license__ = "Apache License, Version 2.0"
