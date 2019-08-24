# Wireless Telemetry Server
Wireless telemetry server for Purdue Electric racing.
Runs on a Raspberry Pi with a connected CANDapter and wireless router.
[Wiki page](http://purdueelectricracing.com/wiki/index.php/Wireless_Telemetry)

## Using pipenv for dependencies
This project uses pipenv to manage dependencies. To install pipenv, run:
`python -m pip install pipenv`

Then, to get all of the packages you need:
`python -m pipenv install`

After that, you're able to activate pipenv by using:
`python -m pipenv shell`

Or, you can run a specific command with:
`python -m pipenv run command`
