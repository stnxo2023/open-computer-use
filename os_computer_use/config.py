# Define the models to use in the agent

from os_computer_use import providers

grounding_model = providers.OSAtlasProvider()
# grounding_model = providers.ShowUIProvider()

# vision_model = providers.FireworksProvider("llama3.2")
# vision_model = providers.GroqProvider("llama3.2")
# vision_model = providers.OpenAIProvider("gpt-4o")
vision_model = providers.AnthropicProvider("claude-3.5-sonnet")

# action_model = providers.FireworksProvider("llama3.3")
# action_model = providers.GroqProvider("llama3.2")
# action_model = providers.OpenAIProvider("gpt-4o")
action_model = providers.AnthropicProvider("claude-3.5-sonnet")