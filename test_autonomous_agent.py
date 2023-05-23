import unittest
from unittest.mock import patch, MagicMock
from agent import AutonomousAgent

class TestAutonomousAgent(unittest.TestCase):

    def setUp(self):
        self.agent = AutonomousAgent("model_id", "test_agent", "test_prompt", "test_folder")

    @patch("openai.ChatCompletion.create")
    def test_send_message(self, mock_create):
        # create a mock response object for openai.ChatCompletion.create
        mock_response = MagicMock()
        mock_response.choices[0].message.content.strip.return_value = "test_response"
        mock_response.usage.total_tokens = 10
        mock_create.return_value = mock_response

        # call the send_message method
        response = self.agent.send_message("test_message")

        # assert that the mock objects were called correctly and that the response was returned
        mock_create.assert_called_with(model="model_id", messages=self.agent.chat_history)
        self.assertEqual(response, "test_response")
        self.assertEqual(self.agent.token, 10)

