#!/usr/bin/env python

# Update current distro information for recipes.
#
# Copyright (C) 2015 Intel Corporation
# Author: Anibal Limon <anibal.limon@linux.intel.com>
#
# Licensed under the MIT license, see COPYING.MIT for details

import sys
import os.path
import optparse
import logging
from datetime import datetime

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__))))
from common import common_setup, update_repo, load_recipes, \
        get_pv_type, get_logger
common_setup()
from layerindex import utils

utils.setup_django()
from django.db import transaction
import settings

logger = get_logger("RecipeDistros", settings)
fetchdir = settings.LAYER_FETCH_DIR
if not fetchdir:
    logger.error("Please set LAYER_FETCH_DIR in settings.py")
    sys.exit(1)

update_repo(settings.LAYER_FETCH_DIR, 'poky', settings.POKY_REPO_URL,
                True, logger)

# setup bitbake path
bitbakepath = os.path.join(fetchdir, 'bitbake')
sys.path.insert(0, os.path.join(bitbakepath, 'lib'))

from layerindex.models import Recipe, LayerBranch
from rrs.models import RecipeDistro

"""
    Searches the recipe's package in major distributions.
    Returns a dictionary containing pairs of (distro name, package aliases).
"""
def search_package_in_distros(pkglst_dir, recipe, data):
    distros = {}
    distro_aliases = {}

    recipe_name = recipe.pn

    removes = ['nativesdk-', '-native', '-cross', '-initial']
    for r in removes:
        recipe_name.replace(r, '')

    distro_alias = data.getVar('DISTRO_PN_ALIAS', True)
    if distro_alias:
        # Gets info from DISTRO_PN_ALIAS into a dictionary containing 
        # the distribution as a key and the package name as value.
        for alias in distro_alias.split():
            if alias.find("=") != -1:
                (dist, pn_alias) = alias.split('=')
                distro_aliases[dist.strip().lower()] = pn_alias.strip()

    for distro_file in os.listdir(pkglst_dir):
        (distro, distro_release) = distro_file.split("-")

        if distro.lower() in distro_aliases:
            pn = distro_aliases[distro.lower()]
        else:
            pn = recipe_name

        f = open(os.path.join(pkglst_dir, distro_file), "rb")
        for line in f:
            (pkg, section) = line.split(":")
            if pn == pkg:
                distro_complete = distro + "-" + section[:-1]
                distros[distro_complete] = pn
                f.close()
                break
        f.close()

    return distros

if __name__=="__main__":
    parser = optparse.OptionParser(usage = """%prog [options]""")
    
    parser.add_option("-d", "--debug",
            help = "Enable debug output",
            action="store_const", const=logging.DEBUG, dest="loglevel", default=logging.INFO)
    
    options, args = parser.parse_args(sys.argv)
    logger.setLevel(options.loglevel)

    logger.debug("Starting recipe distros update ...")

    transaction.enter_transaction_management()
    transaction.managed(True)

    for layerbranch in LayerBranch.objects.all():
        (tinfoil, d, recipes) = load_recipes(layerbranch, bitbakepath,
                fetchdir, settings, logger)

        if not recipes:
            continue

        from oe import distro_check
        logger.debug("Downloading distro's package information ...")
        distro_check.create_distro_packages_list(fetchdir, d)
        pkglst_dir = os.path.join(fetchdir, "package_lists")

        RecipeDistro.objects.filter(recipe__layerbranch = layerbranch).delete()

        for recipe_data in recipes:
            pn = recipe_data.getVar('PN', True)

            try:
                recipe = Recipe.objects.get(pn = pn, layerbranch = layerbranch)
            except:
                logger.warn('%s: layer branch %s, NOT found' % (pn,
                    str(layerbranch)))
                continue

            distro_info = search_package_in_distros(pkglst_dir, recipe, recipe_data)
            for distro, alias in distro_info.items():
                recipedistro = RecipeDistro()
                recipedistro.recipe = recipe
                recipedistro.distro = distro
                recipedistro.alias = alias
                recipedistro.save()
                logger.debug('%s: layer branch %s, add distro %s alias %s' % (pn,
                    str(layerbranch), distro, alias))

    transaction.commit()
    transaction.leave_transaction_management()