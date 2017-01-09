# Script to release the mod into a zip file.
# Assumes BABUN on windows or something like that on Linux (duh)

rm -rf tmp
mkdir tmp

echo "Copying mod files"
git clone . tmp/yupgi_alert
rm -rf tmp/yupgi_alert/{.git,assets,OpenRA.Mods.yupgi_alert}
rm -f tmp/yupgi_alert/.gitignore
rm -f tmp/yupgi_alert/release.sh

# copy the DLL file and the license.
echo "Copying DLL files and license info"
cp OpenRA.Mods.yupgi_alert.dll tmp/yupgi_alert
cp OpenRA.Mods.yupgi_alert/{LICENSE.AS,AUTHORS.AS} tmp/yupgi_alert

# patch mod.yaml
echo "Patching mod.yaml"
cd tmp/yupgi_alert
patch < mod.yaml.patch
rm mod.yaml.patch

# now in tmp dir.
cd ..
echo "Archiving into zip"
zip yupgi_alert.zip -r yupgi_alert
mv yupgi_alert.zip ..
cd ..

echo "Done"
