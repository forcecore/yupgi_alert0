# Script to release the mod into a zip file.
# Assumes BABUN on windows or something like that on Linux (duh)

rm -rf tmp
mkdir tmp

echo "Copying mod files"
git clone . tmp/yupgi_alert
rm -rf tmp/yupgi_alert/{.git,assets,OpenRA.Mods.yupgi_alert,.gitattributes}
rm -f tmp/yupgi_alert/{.gitignore,release.sh}

# copy the DLL file and the license.
echo "Copying DLL files and license info"
cp OpenRA.Mods.yupgi_alert.dll tmp/yupgi_alert
cp ../common/OpenRA.Mods.Common.dll tmp/yupgi_alert/OpenRA.Mods.Uncommon.dll
cp OpenRA.Mods.yupgi_alert/{LICENSE.AS,AUTHORS.AS} tmp/yupgi_alert

# patch mod.yaml
echo "Patching mod.yaml"
cd tmp/yupgi_alert
patch < mod.yaml.patch
rm mod.yaml.patch

# now in tmp dir.
cd ..
echo "Archiving into zip"
cd yupgi_alert
zip ../yupgi_alert.oramod -r *
cd ..
rm -rf yupgi_alert
cp ../LICENSE ../README.md ../ART_CREDITS.txt ../OpenRA.Mods.yupgi_alert/{LICENSE.AS,AUTHORS.AS} .
zip ../yupgi_alert.zip -r *
cd ..

echo "Done"
