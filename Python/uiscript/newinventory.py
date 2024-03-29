import uiScriptLocale
import item
import app
EQUIPMENT_START_INDEX = 0

if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
	BOARD_HEIGHT = 375
	window = {
		"name" : "InventoryWindow",

		"x" : SCREEN_WIDTH - 176,
		"y" : SCREEN_HEIGHT - 37 - BOARD_HEIGHT,

		"style" : ("movable", "float",),

		"width" : 176,
		"height" : BOARD_HEIGHT,

		"children" :
		[
			## Inventory, Equipment Slots
			{
				"name" : "board",
				"type" : "board",
				"style" : ("attach",),

				"x" : 0,
				"y" : 0,

				"width" : 176,
				"height" : BOARD_HEIGHT,

				"children" :
				[
					## Title
					{
						"name" : "TitleBar",
						"type" : "titlebar",
						"style" : ("attach",),

						"x" : 8,
						"y" : 7,

						"width" : 161,
						"color" : "yellow",

						"children" :
						(
							{ "name":"TitleName", "type":"text", "x":77, "y":3, "text":uiScriptLocale.INVENTORY_TITLE, "text_horizontal_align":"center" },
						),
					},
					# Sort
					{
						"name" : "SortBaseImage",
						"type" : "image",
						"style" : ("attach",),

						"x" : 8,
						"y" : 7,

						"image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe.tga",

						"children" :
						(
							# Sort Button (38x24)
							{
								"name" : "SortButton",
								"type" : "button",

								"x" : 11,
								"y" : 3,

								"tooltip_text" : uiScriptLocale.INVENTORY_SORT,

								"default_image" : "d:/ymir work/ui/game/inventory/refresh_small_button_01.sub",
								"over_image" : "d:/ymir work/ui/game/inventory/refresh_small_button_02.sub",
								"down_image" : "d:/ymir work/ui/game/inventory/refresh_small_button_03.sub",
								"disable_image" : "d:/ymir work/ui/game/inventory/refresh_small_button_04.sub",
							},
						),
					},
					{
						"name" : "Inventory_Tab_01",
						"type" : "radio_button",

						"x" : 10,
						"y" : 33,

						"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
						"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_1,

						"children" :
						(
							{
								"name" : "Inventory_Tab_01_Print",
								"type" : "text",

								"x" : 0,
								"y" : 0,

								"all_align" : "center",

								"text" : "I",
							},
						),
					},
					{
						"name" : "Inventory_Tab_02",
						"type" : "radio_button",

						#"x" : 10 + 78,
						"x" : 10 + 39,
						"y" : 33,

						"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
						"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_2,

						"children" :
						(
							{
								"name" : "Inventory_Tab_02_Print",
								"type" : "text",

								"x" : 0,
								"y" : 0,

								"all_align" : "center",

								"text" : "II",
							},
						),
					},
					
					{
						"name" : "Inventory_Tab_03",
						"type" : "radio_button",

						"x" : 10 + 39 + 39,
						"y" : 33,

						"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
						"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_3,

						"children" :
						(
							{
								"name" : "Inventory_Tab_03_Print",
								"type" : "text",

								"x" : 0,
								"y" : 0,

								"all_align" : "center",

								"text" : "III",
							},
						),
					},
					
					{
						"name" : "Inventory_Tab_04",
						"type" : "radio_button",

						"x" : 10 + 39 + 39 + 39,
						"y" : 33,

						"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
						"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_4,

						"children" :
						(
							{
								"name" : "Inventory_Tab_04_Print",
								"type" : "text",

								"x" : 0,
								"y" : 0,

								"all_align" : "center",

								"text" : "IV",
							},
						),
					},

					## Item Slot
					{
						"name" : "ItemSlot",
						"type" : "grid_table",

						"x" : 8,
						"y" : 55,

						"start_index" : 0,
						"x_count" : 5,
						"y_count" : 9,
						"x_step" : 32,
						"y_step" : 32,

						"image" : "d:/ymir work/ui/public/Slot_Base.sub"
					},

					## Print
					{
						"name":"Money_Icon",
						"type":"image",
						"vertical_align":"bottom",
						
						"x":57,
						"y":26,

						"image":"d:/ymir work/ui/game/windows/money_icon.sub",
					},
					{
						"name":"Money_Slot",
						"type":"button",

						"x":75,
						"y":28,

						#"horizontal_align":"center",
						"vertical_align":"bottom",

						"default_image" : "d:/ymir work/ui/public/gold_slot.sub",
						"over_image" : "d:/ymir work/ui/public/gold_slot.sub",
						"down_image" : "d:/ymir work/ui/public/gold_slot.sub",

						"children" :
						(
							{
								"name" : "Money",
								"type" : "text",

								"x" : 3,
								"y" : 3,

								"horizontal_align" : "right",
								"text_horizontal_align" : "right",

								"text" : "123456789",
							},
						),
					},
					#{
					#	"name":"Cheque_Icon",
					#	"type":"image",
					#	"vertical_align":"bottom",
						
					#	"x":10,
					#	"y":26,

					#	"image":"d:/ymir work/ui/game/windows/cheque_icon.sub",
					#},
					#{
					#	"name":"Cheque_Slot",
					#	"type":"button",

					#	"x":28,
					#	"y":28,

						#"horizontal_align":"center",
					#	"vertical_align":"bottom",

					#	"default_image" : "d:/ymir work/ui/public/cheque_slot.sub",
					#	"over_image" : "d:/ymir work/ui/public/cheque_slot.sub",
					#	"down_image" : "d:/ymir work/ui/public/cheque_slot.sub",

					#	"children" :
					#	(
					#		{
					#			"name" : "Cheque",
					#			"type" : "text",

					#			"x" : 3,
					#			"y" : 3,

					#			"horizontal_align" : "right",
					#			"text_horizontal_align" : "right",

					#			"text" : "99",
					#		},
					#	),
					#},
					{
						"name":"Gem_Icon",
						"type":"image",
						
						"x":50 - 98,
						"y":13,
							"image":"d:/ymir work/ui/gemshop/gemshop_gemicon.sub",
					},					
					{
						"name":"Gem_Slot",
						"type":"image",

						"x": 50 - 82,
						"y":10,
							
						"image" : "d:/ymir work/ui/public/Parameter_Slot_01.sub",

						"children" :
						(
							{
								"name" : "Gem",
								"type" : "text",
								"x" : 3,
								"y" : 3,

								"horizontal_align" : "right",
								"text_horizontal_align" : "right",

								"text" : "0",
							},
						),
					},
				],
			},
		],
	}