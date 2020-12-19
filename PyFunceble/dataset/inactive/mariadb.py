"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the interface for the inactive DB (mariadb) management.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from typing import Any, Optional

import sqlalchemy
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

import PyFunceble.cli.factory
from PyFunceble.database.sqlalchemy.all_schemas import Inactive
from PyFunceble.dataset.inactive.base import InactiveDatasetBase
from PyFunceble.dataset.mariadb_base import MariaDBDatasetBase


class MariaDBInactiveDataset(MariaDBDatasetBase, InactiveDatasetBase):
    """
    Provides tht interface for the management and the WHOIS dataset under
    mariadb.
    """

    ORM_OBJ: Inactive = Inactive

    def __contains__(self, value: str) -> bool:
        with PyFunceble.cli.factory.DBSession.get_new_db_session() as db_session:
            return (
                db_session.query(self.ORM_OBJ)
                .filter(
                    self.ORM_OBJ.idna_subject == value,
                )
                .with_entities(sqlalchemy.func.count())
                .scalar()
                > 0
            )

    def __getitem__(self, value: Any) -> Optional[Inactive]:
        with PyFunceble.cli.factory.DBSession.get_new_db_session() as db_session:
            try:
                return (
                    db_session.query(self.ORM_OBJ)
                    .filter(
                        self.ORM_OBJ.idna_subject == value,
                    )
                    .one()
                )
            except NoResultFound:
                return None
            except MultipleResultsFound:
                # Worst case scenario.
                return (
                    db_session.query(self.ORM_OBJ)
                    .filter(
                        self.ORM_OBJ.idna_subject == value,
                    )
                    .all()[0]
                )