echo 'Make sure you have installed curl (sudo apt install curl) and pip3'
echo 'It is also recommended to use a separate virtual environment.'
echo 'Enter your Pushbullet API key (or create one here: https://www.pushbullet.com/#settings/account)'
read PUSHBULLET_API
echo 'Saving it to .bashrc.'
echo 'export PUSHBULLET_API='"'$PUSHBULLET_API'" >> ~/.bashrc

read -r -p "Are you using a Raspberry Pi? [y/N] " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]
then
    pip3 install -r requirements_pi.txt
else
    pip3 install -r requirements.txt
fi

echo "Giving permissions to the alert script."
chmod 777 pushbullet.sh

echo "Sourcing .bashrc.."
source ~/.bashrc

echo 'Sending a test alert!'
MSG="$1"
curl -u $PUSHBULLET_API: https://api.pushbullet.com/v2/pushes -d type=note -d title="Alert" -d body="$MSG"
