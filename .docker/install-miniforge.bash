#!/bin/bash
# This downloads and installs a pinned version of miniconda
set -ex

cd $(dirname $0)
MINIFORGE_VERSION=4.8.2-1
# SHA256 for installers can be obtained from https://github.com/conda-forge/miniforge/releases
SHA256SUM="4f897e503bd0edfb277524ca5b6a5b14ad818b3198c2f07a36858b7d88c928db"

URL="https://github.com/conda-forge/miniforge/releases/download/${MINIFORGE_VERSION}/Miniforge3-${MINIFORGE_VERSION}-Linux-x86_64.sh"
INSTALLER_PATH=/tmp/miniforge-installer.sh

# make sure we don't do anything funky with user's $HOME
# since this is run as root
unset HOME

wget --quiet $URL -O ${INSTALLER_PATH}
chmod +x ${INSTALLER_PATH}

# check sha256 checksum
if ! echo "${SHA256SUM}  ${INSTALLER_PATH}" | sha256sum  --quiet -c -; then
    echo "sha256 mismatch for ${INSTALLER_PATH}, exiting!"
    exit 1
fi

bash ${INSTALLER_PATH} -b -p ${CONDA_DIR}
export PATH="${CONDA_DIR}/bin:$PATH"

# Preserve behavior of miniconda - packages come from conda-forge + defaults
conda config --system --append channels defaults
conda config --system --append channels terradue
conda config --system --append channels r

# Do not attempt to auto update conda or dependencies
conda config --system --set auto_update_conda false
conda config --system --set show_channel_urls true

# bug in conda 4.3.>15 prevents --set update_dependencies
echo 'update_dependencies: false' >> ${CONDA_DIR}/.condarc

# avoid future changes to default channel_priority behavior
conda config --system --set channel_priority "flexible"

echo "installing conda env:"
cat /tmp/environment.yml
conda env create -p ${NB_PYTHON_PREFIX} -f /tmp/environment.yml


# empty conda history file,
# which seems to result in some effective pinning of packages in the initial env,
# which we don't intend.
# this file must not be *removed*, however
echo '' > ${NB_PYTHON_PREFIX}/conda-meta/history

# Clean things out!
conda clean --all -f -y

# Remove the big installer so we don't increase docker image size too much
rm ${INSTALLER_PATH}

# Remove the pip cache created as part of installing miniforge
rm -rf /root/.cache

chown -R $NB_USER:$NB_GID ${CONDA_DIR}

conda list -n root
conda list -p ${NB_PYTHON_PREFIX}

