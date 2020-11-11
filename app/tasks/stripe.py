####################################################################################################
#
# POC - 
# Copyright (C) 2020 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

from invoke import task

from .common import load_settings

####################################################################################################

@task()
def forward_webhook(ctx, env_path="./dev.env"):
    """Forward Stripe webhook"""
    settings = load_settings(env_path)
    host = settings.SERVER_HOST
    port = settings.SERVER_PORT
    url = "/".join((settings.API_V1_STR, "stripe_webhook"))
    ctx.run(f"stripe listen --forward-to {host}:{port}/{url}")
