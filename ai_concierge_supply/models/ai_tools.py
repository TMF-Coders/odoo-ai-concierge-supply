from odoo import models
import logging

_logger = logging.getLogger(__name__)

class AiTools(models.AbstractModel):
    _inherit = 'ai.concierge.tools'

    def get_odoo_tools(self):
        """
        Extends the AI Concierge with Supply Chain specific tools.
        """
        tools = super().get_odoo_tools()

        def get_supply_recommendation(product_id: int) -> str:
            """
            Analyzes the supply forecast for a specific product and provides 
            AI-driven inventory recommendations (e.g., safety stock adjustments).
            
            Args:
                product_id: The integer ID of the product template or product product.
            """
            try:
                # We prioritize product.product but handle template if needed
                product = self.env['product.product'].browse(product_id)
                if not product.exists():
                    template = self.env['product.template'].browse(product_id)
                    if template.exists():
                        product = template.product_variant_id
                
                if not product or not product.exists():
                    return f"Error: Product with ID {product_id} not found."

                # Fetch recent AI-generated forecasts
                forecasts = self.env['supply.forecast'].search_read(
                    [
                        ('product_id', '=', product.id), 
                        ('state', 'in', ['draft', 'confirmed']),
                        ('model_type', '=', 'ai')
                    ],
                    ['date_start', 'forecast_qty'],
                    limit=6,
                    order='date_start asc'
                )

                if not forecasts:
                    return (f"AI Insight for {product.name}: No AI forecasts found yet. "
                            f"I recommend triggering 'Generate AI Forecast' from the supply dashboard first.")

                # Basic Analytics
                total_forecast = sum(f['forecast_qty'] for f in forecasts)
                avg_forecast = total_forecast / len(forecasts)
                
                # Logic to suggest safety stock increase if demand is high
                recommendation = f"Supply Analysis for {product.name}:\n"
                recommendation += f"- Period: Next {len(forecasts)} months\n"
                recommendation += f"- Avg Forecasted Demand: {avg_forecast:.2f} units/month\n"
                
                if avg_forecast > 50: # Example logic
                    recommendation += ("- ACTION: Demand is expected to be high. I suggest increasing the safety stock "
                                       "by 20% to mitigate potential logistics delays.")
                else:
                    recommendation += "- ACTION: Demand is stable. No immediate safety stock adjustment needed."
                
                return recommendation

            except Exception as e:
                _logger.error("AI Supply Tool failed: %s", str(e))
                return f"Execution Error in supply tool: {str(e)}"

        tools['get_supply_recommendation'] = get_supply_recommendation
        return tools
