# Script to release the mod into a zip file.
# Assumes NSIS installer in the new Open RA Mod SDK

# Stop on error.
set -e

if [ $# -eq 0 ] ; then
    echo "Provide release number"
    exit 1
fi

REL=$1
ORA_PATH=/sdk/engine
PREFIX=/sdk/mods/yupgi_alert

echo Cleaning $PREFIX
rm -rf $PREFIX
mkdir -p $PREFIX

echo "Copying mod files"
git clone . $PREFIX

# Remove development files
rm -rf $PREFIX/{.git,assets,.gitattributes}
rm -f $PREFIX/{.gitignore,release.sh}
rm -f $PREFIX/rules/*.py
rm -f $PREFIX/*.py

# copy the DLL file and the license.
echo "Copying license info"
cp LICENSE README.md ART_CREDITS.txt $PREFIX
cp $ORA_PATH/OpenRA.Mods.yupgi_alert/{LICENSE.AS,AUTHORS.AS} $PREFIX

# Convert license to dos line ending. (Notepad is so bad and Linux is more forgiving.)
for f in $PREFIX/{LICENSE,README.md,ART_CREDITS.txt,LICENSE.AS,AUTHORS.AS} ; do
    todos $f
done

# patch mod.yaml
python3 make_mod_yaml.py mod.yaml $REL > $PREFIX/mod.yaml

echo Done. Things are at $PREFIX
