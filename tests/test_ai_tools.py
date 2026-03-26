from odoo.tests.common import TransactionCase

class TestAiConciergeSupply(TransactionCase):
    def setUp(self):
        super(TestAiConciergeSupply, self).setUp()
        self.AiTools = self.env['ai.concierge.tools']

    def test_tool_registration(self):
        """Test if the supply forecast tool is registered."""
        # Simple test to verify the model can be instantiated and the code is structurally sound
        self.assertTrue(hasattr(self.AiTools, 'get_supply_forecast'), "Tool get_supply_forecast should be defined")
