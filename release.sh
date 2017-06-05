# Script to release the mod into a zip file.
# Assumes BABUN on windows or something like that on Linux (duh)

PREFIX=`pwd`/tmp/yupgi_alert
rm -rf tmp
rm -f yupgi_alert.zip
mkdir -p $PREFIX

echo "Copying mod files"
git clone . $PREFIX/oramod

# Remove development files
rm -rf $PREFIX/oramod/{.git,assets,.gitattributes}
rm -f $PREFIX/oramod/{.gitignore,release.sh}
rm -f $PREFIX/oramod/rules/buildpal_order.py
# Remove maps to prevent crash haha
#rm -rf $PREFIX/oramod/maps

# copy the DLL file and the license.
echo "Copying DLL files and license info"
cp OpenRA.Mods.yupgi_alert.dll $PREFIX/oramod
cp ../common/OpenRA.Mods.Common.dll $PREFIX/oramod/OpenRA.Mods.Uncommon.dll
cp LICENSE README.md ART_CREDITS.txt $PREFIX
cp run_opmod.cmd $PREFIX
cp ../../OpenRA.Game.exe $PREFIX/OpenRA.YA.exe
cp ../../OpenRA.Mods.yupgi_alert/{LICENSE.AS,AUTHORS.AS} $PREFIX

# patch mod.yaml
mv $PREFIX/oramod/mod.yaml.release $PREFIX/oramod/mod.yaml

# now in tmp dir,
echo "Archiving into zip"
cd $PREFIX/oramod
zip ../yupgi_alert.oramod -m -r *
cd $PREFIX/..
rmdir $PREFIX/oramod
zip ../yupgi_alert.zip -r yupgi_alert/

echo "Done"
