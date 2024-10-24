\* NXP_trial *\
Minimize
OBJ: 10000 order_delay_0_1 + 10000 order_delay_0_2 + 10000 order_delay_10_1
 + 10000 order_delay_10_2 + 10000 order_delay_11_0 + 10000 order_delay_11_1
 + 10000 order_delay_11_2 + 10000 order_delay_12_1 + 10000 order_delay_12_2
 + 10000 order_delay_13_0 + 10000 order_delay_13_1 + 10000 order_delay_13_2
 + 10000 order_delay_14_1 + 10000 order_delay_14_2 + 10000 order_delay_15_1
 + 10000 order_delay_15_2 + 10000 order_delay_16_2 + 10000 order_delay_17_0
 + 10000 order_delay_17_1 + 10000 order_delay_17_2 + 10000 order_delay_18_2
 + 10000 order_delay_19_0 + 10000 order_delay_19_1 + 10000 order_delay_19_2
 + 10000 order_delay_1_0 + 10000 order_delay_1_1 + 10000 order_delay_1_2
 + 10000 order_delay_20_0 + 10000 order_delay_20_1 + 10000 order_delay_20_2
 + 10000 order_delay_21_2 + 10000 order_delay_22_1 + 10000 order_delay_22_2
 + 10000 order_delay_23_1 + 10000 order_delay_23_2 + 10000 order_delay_24_0
 + 10000 order_delay_24_1 + 10000 order_delay_24_2 + 10000 order_delay_25_1
 + 10000 order_delay_25_2 + 10000 order_delay_26_2 + 10000 order_delay_27_1
 + 10000 order_delay_27_2 + 10000 order_delay_28_1 + 10000 order_delay_28_2
 + 10000 order_delay_29_0 + 10000 order_delay_29_1 + 10000 order_delay_29_2
 + 10000 order_delay_2_1 + 10000 order_delay_2_2 + 10000 order_delay_3_1
 + 10000 order_delay_3_2 + 10000 order_delay_4_0 + 10000 order_delay_4_1
 + 10000 order_delay_4_2 + 10000 order_delay_5_1 + 10000 order_delay_5_2
 + 10000 order_delay_6_2 + 10000 order_delay_7_2 + 10000 order_delay_8_0
 + 10000 order_delay_8_1 + 10000 order_delay_8_2 + 10000 order_delay_9_0
 + 10000 order_delay_9_1 + 10000 order_delay_9_2 + 0.4 resource_production_0_0
 + 0.4 resource_production_0_1 + 0.4 resource_production_0_2
 + 0.3 resource_production_1_0 + 0.3 resource_production_1_1
 + 0.3 resource_production_1_2
Subject To
Order_0_delay_in_1: order_delay_0_1 + order_fulfillment_0_0
 + order_fulfillment_0_1 >= 1
Order_0_delay_in_2: order_delay_0_2 + order_fulfillment_0_0
 + order_fulfillment_0_1 + order_fulfillment_0_2 >= 1
Order_10_delay_in_1: order_delay_10_1 + order_fulfillment_10_0
 + order_fulfillment_10_1 >= 1
Order_10_delay_in_2: order_delay_10_2 + order_fulfillment_10_0
 + order_fulfillment_10_1 + order_fulfillment_10_2 >= 1
Order_11_delay_in_0: order_delay_11_0 + order_fulfillment_11_0 >= 1
Order_11_delay_in_1: order_delay_11_1 + order_fulfillment_11_0
 + order_fulfillment_11_1 >= 1
Order_11_delay_in_2: order_delay_11_2 + order_fulfillment_11_0
 + order_fulfillment_11_1 + order_fulfillment_11_2 >= 1
Order_12_delay_in_1: order_delay_12_1 + order_fulfillment_12_0
 + order_fulfillment_12_1 >= 1
Order_12_delay_in_2: order_delay_12_2 + order_fulfillment_12_0
 + order_fulfillment_12_1 + order_fulfillment_12_2 >= 1
Order_13_delay_in_0: order_delay_13_0 + order_fulfillment_13_0 >= 1
Order_13_delay_in_1: order_delay_13_1 + order_fulfillment_13_0
 + order_fulfillment_13_1 >= 1
Order_13_delay_in_2: order_delay_13_2 + order_fulfillment_13_0
 + order_fulfillment_13_1 + order_fulfillment_13_2 >= 1
Order_14_delay_in_1: order_delay_14_1 + order_fulfillment_14_0
 + order_fulfillment_14_1 >= 1
Order_14_delay_in_2: order_delay_14_2 + order_fulfillment_14_0
 + order_fulfillment_14_1 + order_fulfillment_14_2 >= 1
Order_15_delay_in_1: order_delay_15_1 + order_fulfillment_15_0
 + order_fulfillment_15_1 >= 1
Order_15_delay_in_2: order_delay_15_2 + order_fulfillment_15_0
 + order_fulfillment_15_1 + order_fulfillment_15_2 >= 1
Order_16_delay_in_2: order_delay_16_2 + order_fulfillment_16_0
 + order_fulfillment_16_1 + order_fulfillment_16_2 >= 1
Order_17_delay_in_0: order_delay_17_0 + order_fulfillment_17_0 >= 1
Order_17_delay_in_1: order_delay_17_1 + order_fulfillment_17_0
 + order_fulfillment_17_1 >= 1
Order_17_delay_in_2: order_delay_17_2 + order_fulfillment_17_0
 + order_fulfillment_17_1 + order_fulfillment_17_2 >= 1
Order_18_delay_in_2: order_delay_18_2 + order_fulfillment_18_0
 + order_fulfillment_18_1 + order_fulfillment_18_2 >= 1
Order_19_delay_in_0: order_delay_19_0 + order_fulfillment_19_0 >= 1
Order_19_delay_in_1: order_delay_19_1 + order_fulfillment_19_0
 + order_fulfillment_19_1 >= 1
Order_19_delay_in_2: order_delay_19_2 + order_fulfillment_19_0
 + order_fulfillment_19_1 + order_fulfillment_19_2 >= 1
Order_1_delay_in_0: order_delay_1_0 + order_fulfillment_1_0 >= 1
Order_1_delay_in_1: order_delay_1_1 + order_fulfillment_1_0
 + order_fulfillment_1_1 >= 1
Order_1_delay_in_2: order_delay_1_2 + order_fulfillment_1_0
 + order_fulfillment_1_1 + order_fulfillment_1_2 >= 1
Order_20_delay_in_0: order_delay_20_0 + order_fulfillment_20_0 >= 1
Order_20_delay_in_1: order_delay_20_1 + order_fulfillment_20_0
 + order_fulfillment_20_1 >= 1
Order_20_delay_in_2: order_delay_20_2 + order_fulfillment_20_0
 + order_fulfillment_20_1 + order_fulfillment_20_2 >= 1
Order_21_delay_in_2: order_delay_21_2 + order_fulfillment_21_0
 + order_fulfillment_21_1 + order_fulfillment_21_2 >= 1
Order_22_delay_in_1: order_delay_22_1 + order_fulfillment_22_0
 + order_fulfillment_22_1 >= 1
Order_22_delay_in_2: order_delay_22_2 + order_fulfillment_22_0
 + order_fulfillment_22_1 + order_fulfillment_22_2 >= 1
Order_23_delay_in_1: order_delay_23_1 + order_fulfillment_23_0
 + order_fulfillment_23_1 >= 1
Order_23_delay_in_2: order_delay_23_2 + order_fulfillment_23_0
 + order_fulfillment_23_1 + order_fulfillment_23_2 >= 1
Order_24_delay_in_0: order_delay_24_0 + order_fulfillment_24_0 >= 1
Order_24_delay_in_1: order_delay_24_1 + order_fulfillment_24_0
 + order_fulfillment_24_1 >= 1
Order_24_delay_in_2: order_delay_24_2 + order_fulfillment_24_0
 + order_fulfillment_24_1 + order_fulfillment_24_2 >= 1
Order_25_delay_in_1: order_delay_25_1 + order_fulfillment_25_0
 + order_fulfillment_25_1 >= 1
Order_25_delay_in_2: order_delay_25_2 + order_fulfillment_25_0
 + order_fulfillment_25_1 + order_fulfillment_25_2 >= 1
Order_26_delay_in_2: order_delay_26_2 + order_fulfillment_26_0
 + order_fulfillment_26_1 + order_fulfillment_26_2 >= 1
Order_27_delay_in_1: order_delay_27_1 + order_fulfillment_27_0
 + order_fulfillment_27_1 >= 1
Order_27_delay_in_2: order_delay_27_2 + order_fulfillment_27_0
 + order_fulfillment_27_1 + order_fulfillment_27_2 >= 1
Order_28_delay_in_1: order_delay_28_1 + order_fulfillment_28_0
 + order_fulfillment_28_1 >= 1
Order_28_delay_in_2: order_delay_28_2 + order_fulfillment_28_0
 + order_fulfillment_28_1 + order_fulfillment_28_2 >= 1
Order_29_delay_in_0: order_delay_29_0 + order_fulfillment_29_0 >= 1
Order_29_delay_in_1: order_delay_29_1 + order_fulfillment_29_0
 + order_fulfillment_29_1 >= 1
Order_29_delay_in_2: order_delay_29_2 + order_fulfillment_29_0
 + order_fulfillment_29_1 + order_fulfillment_29_2 >= 1
Order_2_delay_in_1: order_delay_2_1 + order_fulfillment_2_0
 + order_fulfillment_2_1 >= 1
Order_2_delay_in_2: order_delay_2_2 + order_fulfillment_2_0
 + order_fulfillment_2_1 + order_fulfillment_2_2 >= 1
Order_3_delay_in_1: order_delay_3_1 + order_fulfillment_3_0
 + order_fulfillment_3_1 >= 1
Order_3_delay_in_2: order_delay_3_2 + order_fulfillment_3_0
 + order_fulfillment_3_1 + order_fulfillment_3_2 >= 1
Order_4_delay_in_0: order_delay_4_0 + order_fulfillment_4_0 >= 1
Order_4_delay_in_1: order_delay_4_1 + order_fulfillment_4_0
 + order_fulfillment_4_1 >= 1
Order_4_delay_in_2: order_delay_4_2 + order_fulfillment_4_0
 + order_fulfillment_4_1 + order_fulfillment_4_2 >= 1
Order_5_delay_in_1: order_delay_5_1 + order_fulfillment_5_0
 + order_fulfillment_5_1 >= 1
Order_5_delay_in_2: order_delay_5_2 + order_fulfillment_5_0
 + order_fulfillment_5_1 + order_fulfillment_5_2 >= 1
Order_6_delay_in_2: order_delay_6_2 + order_fulfillment_6_0
 + order_fulfillment_6_1 + order_fulfillment_6_2 >= 1
Order_7_delay_in_2: order_delay_7_2 + order_fulfillment_7_0
 + order_fulfillment_7_1 + order_fulfillment_7_2 >= 1
Order_8_delay_in_0: order_delay_8_0 + order_fulfillment_8_0 >= 1
Order_8_delay_in_1: order_delay_8_1 + order_fulfillment_8_0
 + order_fulfillment_8_1 >= 1
Order_8_delay_in_2: order_delay_8_2 + order_fulfillment_8_0
 + order_fulfillment_8_1 + order_fulfillment_8_2 >= 1
Order_9_delay_in_0: order_delay_9_0 + order_fulfillment_9_0 >= 1
Order_9_delay_in_1: order_delay_9_1 + order_fulfillment_9_0
 + order_fulfillment_9_1 >= 1
Order_9_delay_in_2: order_delay_9_2 + order_fulfillment_9_0
 + order_fulfillment_9_1 + order_fulfillment_9_2 >= 1
Order_fulfill_0_0: 255 order_fulfillment_0_0 + 611 order_fulfillment_10_0
 + 435 order_fulfillment_11_0 + 574 order_fulfillment_12_0
 + 669 order_fulfillment_13_0 + 442 order_fulfillment_14_0
 + 440 order_fulfillment_15_0 + 373 order_fulfillment_16_0
 + 124 order_fulfillment_17_0 + 571 order_fulfillment_18_0
 + 489 order_fulfillment_19_0 + 88 order_fulfillment_1_0
 + 654 order_fulfillment_20_0 + 428 order_fulfillment_21_0
 + 705 order_fulfillment_22_0 + 238 order_fulfillment_23_0
 + 405 order_fulfillment_24_0 + 236 order_fulfillment_25_0
 + 330 order_fulfillment_26_0 + 160 order_fulfillment_27_0
 + 152 order_fulfillment_28_0 + 464 order_fulfillment_29_0
 + 403 order_fulfillment_2_0 + 120 order_fulfillment_3_0
 + 511 order_fulfillment_4_0 + 146 order_fulfillment_5_0
 + 574 order_fulfillment_6_0 + 690 order_fulfillment_7_0
 + 466 order_fulfillment_8_0 + 681 order_fulfillment_9_0
 - resource_production_0_0 - starting_inventory_0_0 + starting_inventory_0_1
 = 0
Order_fulfill_0_1: 255 order_fulfillment_0_1 + 611 order_fulfillment_10_1
 + 435 order_fulfillment_11_1 + 574 order_fulfillment_12_1
 + 669 order_fulfillment_13_1 + 442 order_fulfillment_14_1
 + 440 order_fulfillment_15_1 + 373 order_fulfillment_16_1
 + 124 order_fulfillment_17_1 + 571 order_fulfillment_18_1
 + 489 order_fulfillment_19_1 + 88 order_fulfillment_1_1
 + 654 order_fulfillment_20_1 + 428 order_fulfillment_21_1
 + 705 order_fulfillment_22_1 + 238 order_fulfillment_23_1
 + 405 order_fulfillment_24_1 + 236 order_fulfillment_25_1
 + 330 order_fulfillment_26_1 + 160 order_fulfillment_27_1
 + 152 order_fulfillment_28_1 + 464 order_fulfillment_29_1
 + 403 order_fulfillment_2_1 + 120 order_fulfillment_3_1
 + 511 order_fulfillment_4_1 + 146 order_fulfillment_5_1
 + 574 order_fulfillment_6_1 + 690 order_fulfillment_7_1
 + 466 order_fulfillment_8_1 + 681 order_fulfillment_9_1
 - resource_production_0_1 - starting_inventory_0_1 + starting_inventory_0_2
 = 0
Order_fulfill_0_2: 255 order_fulfillment_0_2 + 611 order_fulfillment_10_2
 + 435 order_fulfillment_11_2 + 574 order_fulfillment_12_2
 + 669 order_fulfillment_13_2 + 442 order_fulfillment_14_2
 + 440 order_fulfillment_15_2 + 373 order_fulfillment_16_2
 + 124 order_fulfillment_17_2 + 571 order_fulfillment_18_2
 + 489 order_fulfillment_19_2 + 88 order_fulfillment_1_2
 + 654 order_fulfillment_20_2 + 428 order_fulfillment_21_2
 + 705 order_fulfillment_22_2 + 238 order_fulfillment_23_2
 + 405 order_fulfillment_24_2 + 236 order_fulfillment_25_2
 + 330 order_fulfillment_26_2 + 160 order_fulfillment_27_2
 + 152 order_fulfillment_28_2 + 464 order_fulfillment_29_2
 + 403 order_fulfillment_2_2 + 120 order_fulfillment_3_2
 + 511 order_fulfillment_4_2 + 146 order_fulfillment_5_2
 + 574 order_fulfillment_6_2 + 690 order_fulfillment_7_2
 + 466 order_fulfillment_8_2 + 681 order_fulfillment_9_2
 - resource_production_0_2 - starting_inventory_0_2 + starting_inventory_0_3
 = 0
Order_fulfill_1_0: 102 order_fulfillment_0_0 + 96 order_fulfillment_12_0
 + 66 order_fulfillment_14_0 + 60 order_fulfillment_15_0
 + 108 order_fulfillment_17_0 + 78 order_fulfillment_18_0
 + 78 order_fulfillment_19_0 + 84 order_fulfillment_1_0
 + 90 order_fulfillment_23_0 + 66 order_fulfillment_24_0
 + 96 order_fulfillment_25_0 + 72 order_fulfillment_28_0
 + 108 order_fulfillment_29_0 + 96 order_fulfillment_3_0
 + 120 order_fulfillment_4_0 + 102 order_fulfillment_5_0
 + 84 order_fulfillment_8_0 + 72 order_fulfillment_9_0
 - resource_production_1_0 - starting_inventory_1_0 + starting_inventory_1_1
 = 0
Order_fulfill_1_1: 102 order_fulfillment_0_1 + 96 order_fulfillment_12_1
 + 66 order_fulfillment_14_1 + 60 order_fulfillment_15_1
 + 108 order_fulfillment_17_1 + 78 order_fulfillment_18_1
 + 78 order_fulfillment_19_1 + 84 order_fulfillment_1_1
 + 90 order_fulfillment_23_1 + 66 order_fulfillment_24_1
 + 96 order_fulfillment_25_1 + 72 order_fulfillment_28_1
 + 108 order_fulfillment_29_1 + 96 order_fulfillment_3_1
 + 120 order_fulfillment_4_1 + 102 order_fulfillment_5_1
 + 84 order_fulfillment_8_1 + 72 order_fulfillment_9_1
 - resource_production_1_1 - starting_inventory_1_1 + starting_inventory_1_2
 = 0
Order_fulfill_1_2: 102 order_fulfillment_0_2 + 96 order_fulfillment_12_2
 + 66 order_fulfillment_14_2 + 60 order_fulfillment_15_2
 + 108 order_fulfillment_17_2 + 78 order_fulfillment_18_2
 + 78 order_fulfillment_19_2 + 84 order_fulfillment_1_2
 + 90 order_fulfillment_23_2 + 66 order_fulfillment_24_2
 + 96 order_fulfillment_25_2 + 72 order_fulfillment_28_2
 + 108 order_fulfillment_29_2 + 96 order_fulfillment_3_2
 + 120 order_fulfillment_4_2 + 102 order_fulfillment_5_2
 + 84 order_fulfillment_8_2 + 72 order_fulfillment_9_2
 - resource_production_1_2 - starting_inventory_1_2 + starting_inventory_1_3
 = 0
Resource_cap_resource_0_time_0: resource_production_0_0 <= 3523
Resource_cap_resource_0_time_1: resource_production_0_1 <= 3523
Resource_cap_resource_0_time_2: resource_production_0_2 <= 3523
Resource_cap_resource_1_time_0: resource_production_1_0 <= 447
Resource_cap_resource_1_time_1: resource_production_1_1 <= 447
Resource_cap_resource_1_time_2: resource_production_1_2 <= 447
_C1: starting_inventory_0_0 <= 0
_C2: starting_inventory_1_0 <= 0
Binaries
order_delay_0_1
order_delay_0_2
order_delay_10_1
order_delay_10_2
order_delay_11_0
order_delay_11_1
order_delay_11_2
order_delay_12_1
order_delay_12_2
order_delay_13_0
order_delay_13_1
order_delay_13_2
order_delay_14_1
order_delay_14_2
order_delay_15_1
order_delay_15_2
order_delay_16_2
order_delay_17_0
order_delay_17_1
order_delay_17_2
order_delay_18_2
order_delay_19_0
order_delay_19_1
order_delay_19_2
order_delay_1_0
order_delay_1_1
order_delay_1_2
order_delay_20_0
order_delay_20_1
order_delay_20_2
order_delay_21_2
order_delay_22_1
order_delay_22_2
order_delay_23_1
order_delay_23_2
order_delay_24_0
order_delay_24_1
order_delay_24_2
order_delay_25_1
order_delay_25_2
order_delay_26_2
order_delay_27_1
order_delay_27_2
order_delay_28_1
order_delay_28_2
order_delay_29_0
order_delay_29_1
order_delay_29_2
order_delay_2_1
order_delay_2_2
order_delay_3_1
order_delay_3_2
order_delay_4_0
order_delay_4_1
order_delay_4_2
order_delay_5_1
order_delay_5_2
order_delay_6_2
order_delay_7_2
order_delay_8_0
order_delay_8_1
order_delay_8_2
order_delay_9_0
order_delay_9_1
order_delay_9_2
order_fulfillment_0_0
order_fulfillment_0_1
order_fulfillment_0_2
order_fulfillment_10_0
order_fulfillment_10_1
order_fulfillment_10_2
order_fulfillment_11_0
order_fulfillment_11_1
order_fulfillment_11_2
order_fulfillment_12_0
order_fulfillment_12_1
order_fulfillment_12_2
order_fulfillment_13_0
order_fulfillment_13_1
order_fulfillment_13_2
order_fulfillment_14_0
order_fulfillment_14_1
order_fulfillment_14_2
order_fulfillment_15_0
order_fulfillment_15_1
order_fulfillment_15_2
order_fulfillment_16_0
order_fulfillment_16_1
order_fulfillment_16_2
order_fulfillment_17_0
order_fulfillment_17_1
order_fulfillment_17_2
order_fulfillment_18_0
order_fulfillment_18_1
order_fulfillment_18_2
order_fulfillment_19_0
order_fulfillment_19_1
order_fulfillment_19_2
order_fulfillment_1_0
order_fulfillment_1_1
order_fulfillment_1_2
order_fulfillment_20_0
order_fulfillment_20_1
order_fulfillment_20_2
order_fulfillment_21_0
order_fulfillment_21_1
order_fulfillment_21_2
order_fulfillment_22_0
order_fulfillment_22_1
order_fulfillment_22_2
order_fulfillment_23_0
order_fulfillment_23_1
order_fulfillment_23_2
order_fulfillment_24_0
order_fulfillment_24_1
order_fulfillment_24_2
order_fulfillment_25_0
order_fulfillment_25_1
order_fulfillment_25_2
order_fulfillment_26_0
order_fulfillment_26_1
order_fulfillment_26_2
order_fulfillment_27_0
order_fulfillment_27_1
order_fulfillment_27_2
order_fulfillment_28_0
order_fulfillment_28_1
order_fulfillment_28_2
order_fulfillment_29_0
order_fulfillment_29_1
order_fulfillment_29_2
order_fulfillment_2_0
order_fulfillment_2_1
order_fulfillment_2_2
order_fulfillment_3_0
order_fulfillment_3_1
order_fulfillment_3_2
order_fulfillment_4_0
order_fulfillment_4_1
order_fulfillment_4_2
order_fulfillment_5_0
order_fulfillment_5_1
order_fulfillment_5_2
order_fulfillment_6_0
order_fulfillment_6_1
order_fulfillment_6_2
order_fulfillment_7_0
order_fulfillment_7_1
order_fulfillment_7_2
order_fulfillment_8_0
order_fulfillment_8_1
order_fulfillment_8_2
order_fulfillment_9_0
order_fulfillment_9_1
order_fulfillment_9_2
End
