import app
import item

import player

EQUIPMENT_START_INDEX = player.EQUIPMENT_SLOT_START
COSTUME_START_INDEX = item.COSTUME_SLOT_START

PUBLIC_PATH = "d:/ymir work/ui/public/"

SLOT_INDEX_JOB		= item.PASSIVE_ATTR_SLOT_INDEX_JOB		#m2netm2g.PASSIVE_ATTR_SLOT_INDEX_JOB
SLOT_INDEX_WEAPON	= item.PASSIVE_ATTR_SLOT_INDEX_WEAPON		#m2netm2g.PASSIVE_ATTR_SLOT_INDEX_WEAPON
SLOT_INDEX_ELEMENT	= item.PASSIVE_ATTR_SLOT_INDEX_ELEMENT		#m2netm2g.PASSIVE_ATTR_SLOT_INDEX_ELEMENT
SLOT_INDEX_ARMOR	= item.PASSIVE_ATTR_SLOT_INDEX_ARMOR		#m2netm2g.PASSIVE_ATTR_SLOT_INDEX_ARMOR
SLOT_INDEX_ACCE		= item.PASSIVE_ATTR_SLOT_INDEX_ACCE		#m2netm2g.PASSIVE_ATTR_SLOT_INDEX_ACCE
BG_START_X		= 13
BG_START_Y		= 35

BG_WIDTH		= 172
BG_HEIGHT		= 172

if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
	import uiScriptLocale
	BOARD_WIDTH		= 180
	BOARD_HEIGHT	= 290

	window = {
		"name" : "Equipment",
		"style" : ("movable", "float",),
		
		"x" : SCREEN_WIDTH - 180,
		"y" : SCREEN_HEIGHT - 37 - (BOARD_HEIGHT*2+80),

		"width" : BOARD_WIDTH,
		"height" : BOARD_HEIGHT,

		"children" :
		(
			{
				"name" : "board",
				"type" : "board",
				"style" : ("attach",),
				
				"x" : 0,
				"y" : 0,

				"width" : BOARD_WIDTH,
				"height" : BOARD_HEIGHT,

				#"title" : uiScriptLocale.EQUIPMENT_TITLE_NAME,

				"children" :
				(
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
							{ "name":"TitleName", "type":"text", "x":77, "y":3, "text":uiScriptLocale.EQUIPMENT_TITLE_NAME, "text_horizontal_align":"center" },
						),
					},
					## base_tab
					{
						"name" : "base_tab",
						"type" : "image",

						"x" : 12,
						"y" : 33,

						"width" : BOARD_WIDTH,
						"height" : 25,

						"image" : "d:/ymir work/ui/equipment_bg_without_ring_tab00.tga",
					},
					## Tab Area
					{
						"name" : "additional_tab",
						"type" : "window",

						"x" : 12,
						"y" : 33,

						"width" : BOARD_WIDTH,
						"height" : 26,

						"children" :
						[
							{
								"name" : "tab_img_01",
								"type" : "image",

								"x" : 0,
								"y" : 0,

								"width" : BOARD_WIDTH,
								"height" : 25,

								"image" : "d:/ymir work/ui/equipment_bg_without_ring_tab01.tga",
							},
							{
								"name" : "tab_img_02",
								"type" : "image",

								"x" : 0,
								"y" : 0,

								"width" : BOARD_WIDTH,
								"height" : 25,

								"image" : "d:/ymir work/ui/equipment_bg_without_ring_tab02.tga",
							},
							{
								"name" : "tab_btn_01",
								"type" : "button",

								"x" : 0,
								"y" : 0,

								"width" : 39,
								"height" : 25,
								"tooltip_text" : uiScriptLocale.EQUIPMENT_SLOT_1,
							},
							{
								"name" : "tab_btn_02",
								"type" : "button",

								"x" : 39,
								"y" : 0,

								"width" : 39,
								"height" : 25,
								"tooltip_text" : uiScriptLocale.EQUIPMENT_SLOT_2,
							},
						],
					},
					## wiki_button
					{
						"name" : "wiki_button",
						"type" : "button",

						"x" : 100,
						"y" : 33,

						"tooltip_text" : uiScriptLocale.WIKI_BUTTON,

						"default_image" : "d:/ymir work/ui/special_inventory/wikibutton.png",
						"over_image" : "d:/ymir work/ui/special_inventory/wikibutton.png",
						"down_image" : "d:/ymir work/ui/special_inventory/wikibutton.png",
					},
					## switchbot_button
					{
						"name" : "switchbot_button",
						"type" : "button",

						"x" : 126,
						"y" : 33,

						"tooltip_text" : uiScriptLocale.SWITCHBOT_BUTTON,

						"default_image" : "d:/ymir work/ui/special_inventory/switchbot.png",
						"over_image" : "d:/ymir work/ui/special_inventory/switchbot.png",
						"down_image" : "d:/ymir work/ui/special_inventory/switchbot.png",
					},
					## equip area
					{
						"name" : "equipment_window",
						"type" : "window",

						"x" : 0,
						"y" : 56,

						"width" : BOARD_WIDTH,
						"height" : BOARD_HEIGHT,

						"children" :
						[							
							## equipment slots
							{
								"name":"equipment_base_image",
								"type":"image",
								"style" : ("attach",),

								"x" : 0,
								"y" : 0,
								"horizontal_align" : "center",
								#"image" : "d:/ymir work/ui/new_equipment_bg_without_ring.tga",
								"image" : "d:/ymir work/ui/aeldra_inventory/new_equipment_bg_without_ring_1.tga",

								"children" :
								(
									{
										"name" : "equipment_slot",
										"type" : "slot",

										"x" : 3,
										"y" : 3,

										"width" : 150,
										"height" : 140,

										"slot" : 
										(
											## ARMOR_BODY
											{"index":EQUIPMENT_START_INDEX+0, "x":39, "y":37, "width":32, "height":64},
											## ARMOR_HEAD
											{"index":EQUIPMENT_START_INDEX+1, "x":39, "y":2, "width":32, "height":32},
											## ARMOR_FOOTS
											{"index":EQUIPMENT_START_INDEX+2, "x":4, "y":99, "width":32, "height":32},
											## ARMOR_WRIST
											{"index":EQUIPMENT_START_INDEX+3, "x":75, "y":67, "width":32, "height":32},
											## ITEM_WEAPON
											{"index":EQUIPMENT_START_INDEX+4, "x":3, "y":3, "width":32, "height":96},
											## ARMOR_NECK
											{"index":EQUIPMENT_START_INDEX+5, "x":114, "y":67, "width":32, "height":32},
											## ARMOR_EAR
											{"index":EQUIPMENT_START_INDEX+6, "x":114, "y":35, "width":32, "height":32},
											## WEAPON_QUIVER
											{"index":EQUIPMENT_START_INDEX+9, "x":114, "y":2, "width":32, "height":32},
											## ARMOR_SHIELD
											{"index":EQUIPMENT_START_INDEX+10, "x":75, "y":35, "width":32, "height":32},
											## ITEM_BELT
											{"index":item.EQUIPMENT_BELT, "x":39, "y":99, "width":32, "height":32},
											## ARMOR_PENDANT
											{"index":item.EQUIPMENT_PENDANT, "x":75, "y":2, "width":32, "height":32},
											## ARMOR_GLOVE
											{"index":item.EQUIPMENT_GLOVE, "x":75, "y":99, "width":32, "height":32},
										),
									},
									{
										"name" : "unique_slot",
										"type" : "slot",

										"x" : 3,
										"y" : 140,

										"width" : 150,
										"height" : 36,

										"slot" : 
										(
											## ITEM_UNIQUE_LEFT
											{"index":EQUIPMENT_START_INDEX+7, "x":2, "y":7, "width":32, "height":32},
											## ITEM_UNIQUE_RIGHT
											{"index":EQUIPMENT_START_INDEX+8, "x":39, "y":7, "width":32, "height":32},
										),
									},
								),
							},
							## dragon_soul_button
							{
								"name" : "dragon_soul_button",
								"type" : "button",

								"x" : 18,
								"y" : 186,

								"tooltip_text" : uiScriptLocale.TASKBAR_DRAGON_SOUL,

								"default_image" : "d:/ymir work/ui/dragonsoul/DragonSoul_Button_01.tga",
								"over_image" : "d:/ymir work/ui/dragonsoul/DragonSoul_Button_02.tga",
								"down_image" : "d:/ymir work/ui/dragonsoul/DragonSoul_Button_03.tga",
							},
							## mall_button
							{
								"name" : "mall_button",
								"type" : "button",

								"x" : 53,
								"y" : 186,

								"tooltip_text" : uiScriptLocale.MALL_TITLE,
								
								"default_image" : "d:/ymir work/ui/game/taskbar/Mall_Button_01.tga",
								"over_image" : "d:/ymir work/ui/game/taskbar/Mall_Button_02.tga",
								"down_image" : "d:/ymir work/ui/game/taskbar/Mall_Button_03.tga",
							},
							## premium_private_shop_button
							{
								"name" : "premium_private_shop_button",
								"type" : "button",

								"x" : 91,
								"y" : 186,

								"tooltip_text" : uiScriptLocale.PREMIUM_PRIVATE_SHOP,
								
								"default_image" : "icon/item/private_button_01.tga",
								"over_image" : "icon/item/private_button_02.tga",
								"down_image" : "icon/item/private_button_03.tga",
							},
							## costume_button
							{
								"name" : "costume_button",
								"type" : "button",

								"x" : 132,
								"y" : 186,

								"tooltip_text" : uiScriptLocale.COSTUME_TITLE,

								"default_image" : "d:/ymir work/ui/game/taskbar/ex_gemshop_button_01.tga",
								"over_image" : "d:/ymir work/ui/game/taskbar/ex_gemshop_button_02.tga",
								"down_image" : "d:/ymir work/ui/game/taskbar/ex_gemshop_button_03.tga",
							},	
						],
					},	
				),
			},
		),
	}
	