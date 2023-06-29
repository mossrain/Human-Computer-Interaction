After configuring the rasa project's environment as described in the powerpoint, replace actions/actions.py with the version in the zip package.

The code comments out the part that uses `openai.Completion.create` and leaves the part that uses `openai.ChatCompletion.create`. If you need to switch the APIs, simply replace the commented part.

Open the right python virtual environment in Terminal A. run `rasa run actions`. Open a new terminal B and run `rasa shell`. When terminal B is finished loading and asks the user for input, type `/new_chat`. Then switch to Terminal A, you can see the text prompted to enter, enter whatever you want to enter to start the interaction.