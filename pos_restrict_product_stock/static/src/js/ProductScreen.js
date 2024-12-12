/** @odoo-module **/
/*
 * This file is used to restrict out of stock product from ordering and show restrict popup
 */
import Registries from 'point_of_sale.Registries';
import ProductScreen from 'point_of_sale.ProductScreen';

const RestrictProductScreen = (ProductScreen) => class RestrictProductScreen extends ProductScreen {
    async _clickProduct(event) {
        const product = event.detail;
        var type = this.env.pos.config.stock_type
        if (this.env.pos.config.is_restrict_product && ((type == 'qty_on_hand') && (product.qty_available <= 0)) | ((type == 'virtual_qty') && (product.virtual_available <= 0)) |
            ((product.qty_available <= 0) && (product.virtual_available <= 0))) {
            // If the product restriction is activated in the settings and quantity is out stock, it show the restrict popup.
            this.showPopup("RestrictStockPopup", {
                body: product.display_name,
                pro_id: product.id
            });
        }
        else{
            await super._clickProduct(event)
        }
    }
    async _onClickPay() {
     var type = this.env.pos.config.stock_type
             const pay = true
             const body = []
             const pro_id = false
            for (const line of this.env.pos.selectedOrder.orderlines) {
             if (line.pos.config.is_restrict_product && ((type == 'qty_on_hand') && (line.product.qty_available <= 0)) | ((type == 'virtual_qty') && (line.product.virtual_available <= 0)) |
                                     ((line.product.qty_available <= 0) && (line.product.virtual_available <= 0))) {
                                     // If the product restriction is activated in the settings and quantity is out stock, it show the restrict popup.
                                body.push(line.product.display_name)
                 }
             }
             if (body.length > 0) { // Check if body has items
                     const confirmed = await  this.showPopup("RestrictStockPopup", {
                         body: body,
                         pro_id: pro_id
                     });
                     if (confirmed == true) {
                        return  super._onClickPay(...arguments);// Proceed with payment
                     } else {
                          return ;
                     }
                 } else {
                    return  super._onClickPay(...arguments); // No restrictions, proceed with payment
                 }
             }
}
Registries.Component.extend(ProductScreen, RestrictProductScreen);
