import ui
import player
import mouseModule
import net
import app
import snd
import item
import chat
import grp
import uiScriptLocale
import uiRefine
import uiAttachMetin
import uiPickMoney
import uiCommon
import uiPrivateShopBuilder
import localeInfo
import constInfo
import ime
import wndMgr

import dbg #DEBUG
	
if app.BL_67_ATTR:
	import uiAttr67Add

ITEM_MALL_BUTTON_ENABLE = True

ITEM_FLAG_APPLICABLE = 1 << 14

class CostumeWindow(ui.ScriptWindow):

	def __init__(self, wndInventory):
		import exception

		if not app.ENABLE_COSTUME_SYSTEM:
			exception.Abort("What do you do?")
			return

		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;

		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			self.elemets_world = {}

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		self.RefreshCostumeSlot()

		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/CostumeWindow.py")
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			wndEquip = self.GetChild("CostumeSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))

		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		## Equipment
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))

		self.wndEquip = wndEquip

	def RefreshCostumeSlot(self):
		getItemVNum=player.GetItemIndex

		for i in xrange(item.COSTUME_SLOT_COUNT):
			slotNumber = item.COSTUME_SLOT_START + i
			self.wndEquip.SetItemSlot(slotNumber, getItemVNum(slotNumber), 0)
			if app.BL_TRANSMUTATION_SYSTEM:
				if not player.GetChangeLookVnum(player.EQUIPMENT, slotNumber) == 0:
					self.wndEquip.SetSlotCoverImage(slotNumber,"icon/item/ingame_convert_Mark.tga")
				else:
					self.wndEquip.EnableSlotCoverImage(slotNumber,False)
		if app.ENABLE_WEAPON_COSTUME_SYSTEM:
			self.wndEquip.SetItemSlot(item.COSTUME_SLOT_WEAPON, getItemVNum(item.COSTUME_SLOT_WEAPON), 0)

		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			self.elemets_hide = self.wndInventory.get_costume_hide_list()
			self.ButtonsHideCostume()
			self.costume_hide_load()

		self.wndEquip.RefreshSlot()

class BeltInventoryWindow(ui.ScriptWindow):

	def __init__(self, wndInventory):
		import exception

		if not app.ENABLE_NEW_EQUIPMENT_SYSTEM:
			exception.Abort("What do you do?")
			return

		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;

		self.wndBeltInventoryLayer = None
		self.wndBeltInventorySlot = None
		self.expandBtn = None
		self.minBtn = None
		##activateall
		self.UseItemBelt = None

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self, openBeltSlot = False):
		self.__LoadWindow()
		self.RefreshSlot()

		ui.ScriptWindow.Show(self)

		if openBeltSlot:
			self.OpenInventory()
		else:
			self.CloseInventory()

	def Close(self):
		self.Hide()
		
	def IsOpeningInventory(self):
		return self.wndBeltInventoryLayer.IsShow()

	def OpenInventory(self):
		self.wndBeltInventoryLayer.Show()
		self.expandBtn.Hide()

		if localeInfo.IsARABIC() == 0:
			self.AdjustPositionAndSize()
				
	def CloseInventory(self):
		self.wndBeltInventoryLayer.Hide()
		self.expandBtn.Show()

		if localeInfo.IsARABIC() == 0:
			self.AdjustPositionAndSize()
		
	def GetBasePosition(self):
		x, y = self.wndInventory.GetGlobalPosition()

		return x - 148, y + 80
			
	def AdjustPositionAndSize(self):
		bx, by = self.GetBasePosition()

		if self.IsOpeningInventory():
			self.SetPosition(bx, by)
			self.SetSize(self.ORIGINAL_WIDTH, self.GetHeight())

		else:
			self.SetPosition(bx + 138, by);
			self.SetSize(10, self.GetHeight())

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/BeltInventoryWindow.py")
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			self.ORIGINAL_WIDTH = self.GetWidth()
			wndBeltInventorySlot = self.GetChild("BeltInventorySlot")
			self.wndBeltInventoryLayer = self.GetChild("BeltInventoryLayer")
			self.expandBtn = self.GetChild("ExpandBtn")
			self.minBtn = self.GetChild("MinimizeBtn")
			
			##activateall
			self.UseItemBelt = self.GetChild("UseBeltItemsButton")

			self.expandBtn.SetEvent(ui.__mem_func__(self.OpenInventory))
			self.minBtn.SetEvent(ui.__mem_func__(self.CloseInventory))

			##activateall
			self.UseItemBelt.SetEvent(ui.__mem_func__(self.ActivateAll))
			
			if localeInfo.IsARABIC() :
				self.expandBtn.SetPosition(self.expandBtn.GetWidth() - 2, 15)
				self.wndBeltInventoryLayer.SetPosition(self.wndBeltInventoryLayer.GetWidth() - 5, 0)
				self.minBtn.SetPosition(self.minBtn.GetWidth() + 3, 15)

			for i in xrange(item.BELT_INVENTORY_SLOT_COUNT):
				slotNumber = item.BELT_INVENTORY_SLOT_START + i
				wndBeltInventorySlot.SetCoverButton(slotNumber,	"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/belt_inventory/slot_disabled.tga", False, False)

		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		## Equipment
		wndBeltInventorySlot.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndBeltInventorySlot.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndBeltInventorySlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndBeltInventorySlot.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndBeltInventorySlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		wndBeltInventorySlot.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))

		self.wndBeltInventorySlot = wndBeltInventorySlot

	##activateall
	def ActivateAll(self):
		for i in xrange(item.BELT_INVENTORY_SLOT_COUNT):
			slotNumber = item.BELT_INVENTORY_SLOT_START + i
			net.SendItemUsePacket(slotNumber)
			
	def RefreshSlot(self):
		getItemVNum=player.GetItemIndex

		for i in xrange(item.BELT_INVENTORY_SLOT_COUNT):
			slotNumber = item.BELT_INVENTORY_SLOT_START + i
			self.wndBeltInventorySlot.SetItemSlot(slotNumber, getItemVNum(slotNumber), player.GetItemCount(slotNumber))
			self.wndBeltInventorySlot.SetAlwaysRenderCoverButton(slotNumber, True)

			avail = "0"

			if player.IsAvailableBeltInventoryCell(slotNumber):
				self.wndBeltInventorySlot.EnableCoverButton(slotNumber)
			else:
				self.wndBeltInventorySlot.DisableCoverButton(slotNumber)

		self.wndBeltInventorySlot.RefreshSlot()

class EquipmentWindow(ui.ScriptWindow):
	#Initialice all objects
	isLoaded								= 0
	tooltipItem								= None
	wndCostume								= None
	wndBelt									= None
	questionDialog							= None
	
	isOpenedBeltWindowWhenClosingInventory	= 0
			
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.equipmentTab					= []

		wndEquip							= None
		wndUniqueEquip						= None
		wndDragonSoulButton					= None
		wndMallButton						= None
		wndPremiumPrivateShopButton			= None
		wndCostumeButton					= None
		
		wndOfflineSearchButton2				= None
		wndSwitchBotButton2					= None

		self.wndEquip						= None
		self.wndUniqueEquip					= None
		self.wndDragonSoulButton			= None
		self.wndMallButton					= None
		self.wndPremiumPrivateShopButton	= None
		self.wndCostumeButton				= None

		self.wndOfflineSearchButton2		= None
		self.wndSwitchBotButton2			= None
		
		wndWikiButton						= None
		wndSwitchbotButton					= None
		self.wndWikiButton					= None
		self.wndSwitchbotButton				= None
		
		#Extra variables
		
		self.wndCostume						= None
		self.interface						= None
		self.tooltipItem					= None
		self.questionDialog 				= None
		self.isOpenedBeltWindowWhenClosingInventory = 0
			
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)

		#if self.wndBelt:
		#	self.wndBelt.Show(self.isOpenedBeltWindowWhenClosingInventory)
				
	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
		self.isLoaded = 1
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/NewEquipment.py")
		except:
			import exception
			exception.Abort("EquipmentWindow.LoadWindow.LoadObject")

		try:
			self.BindObject()
		except:
			import exception
			exception.Abort("EquipmentWindow.LoadWindow.BindObject")

	def BindObject(self):
		self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			
		self.equipmentTab			= []
		self.equipmentTab.append(self.GetChild("tab_btn_01"))
		self.equipmentTab.append(self.GetChild("tab_btn_02"))
	
		wndEquip					= self.GetChild("equipment_slot")
		wndUniqueEquip				= self.GetChild("unique_slot")

		wndDragonSoulButton			= self.GetChild("dragon_soul_button")
		wndMallButton				= self.GetChild("mall_button")
		wndPremiumPrivateShopButton = self.GetChild("premium_private_shop_button")
		wndCostumeButton			= self.GetChild("costume_button")

		wndWikiButton					= self.GetChild("wiki_button")
		wndSwitchbotButton				= self.GetChild("switchbot_button")

		wndOfflineSearchButton2			= self.GetChild("offline_search2")
		wndSwitchBotButton2				= self.GetChild("switchbot2")
			
		self.wndBelt					= None
		if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
			self.wndBelt					= BeltInventoryWindow(self)
			
			self.wndBelt.Hide()
		
		self.wndEquip						= wndEquip
		self.wndUniqueEquip					= wndUniqueEquip
		self.wndDragonSoulButton			= wndDragonSoulButton
		self.wndMallButton					= wndMallButton
		self.wndPremiumPrivateShopButton	= wndPremiumPrivateShopButton
		self.wndCostumeButton				= wndCostumeButton
	
		self.wndOfflineSearchButton2		= wndOfflineSearchButton2
		self.wndSwitchBotButton2			= wndSwitchBotButton2
		
		self.wndWikiButton					= wndWikiButton
		self.wndSwitchbotButton				= wndSwitchbotButton
		
		self.wndWikiButton.Hide()
		self.wndSwitchbotButton.Hide()
		
		#Extra variables
		self.wndCostume						= None
		self.inventoryPageIndex 			= 0
		
		self.BindEvent()
		
	def BindEvent(self):
		self.wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		self.wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		self.wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		self.wndEquip.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		self.wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		self.wndUniqueEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		self.wndUniqueEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		self.wndUniqueEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		self.wndUniqueEquip.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		self.wndUniqueEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.wndUniqueEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		
		self.equipmentTab[0].SetEvent(lambda arg=0: self.SetEquipmentPage(arg))
		self.equipmentTab[1].SetEvent(lambda arg=1: self.SetEquipmentPage(arg))
		self.equipmentTab[0].Down()
				
		#DSS Button
		if self.wndDragonSoulButton:
			self.wndDragonSoulButton.SetEvent(ui.__mem_func__(self.ClickDSSButton))
						
		# MallButton
		if self.wndMallButton:
			self.wndMallButton.SetEvent(ui.__mem_func__(self.ClickMallButton))

		# PremiumPrivateShop
		if self.wndPremiumPrivateShopButton:
			self.wndPremiumPrivateShopButton.SetEvent(ui.__mem_func__(self.ClickOfflineButton))

		# Costume Button
		if self.wndCostumeButton:
			self.wndCostumeButton.SetEvent(ui.__mem_func__(self.ClickCostumeButton))
		
		if self.wndWikiButton:
			self.wndWikiButton.SetEvent(ui.__mem_func__(self.ClickWikiButton))
			
		if self.wndSwitchbotButton:
			self.wndSwitchbotButton.SetEvent(ui.__mem_func__(self.ClickSwitchButton))

		if self.wndOfflineSearchButton2:
			self.wndOfflineSearchButton2.SetEvent(ui.__mem_func__(self.ClickSearchButton))
			
		if self.wndSwitchBotButton2:
			self.wndSwitchBotButton2.SetEvent(ui.__mem_func__(self.ClickSwitchButton))
				
		#Refresh
		self.SetEquipmentPage(0)

	#Destroy and close all objects		
	def Hide(self):
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		#if self.wndCostume:
		#	self.isOpenedCostumeWindowWhenClosingInventory = self.wndCostume.IsShow()			# ???? ?? ?? ? ???? ?? ?????
		#	self.wndCostume.Close()

		if self.wndBelt:
			self.isOpenedBeltWindowWhenClosingInventory = self.wndBelt.IsOpeningInventory()		# ???? ?? ?? ? ?? ????? ?? ?????
			print "Is Opening Belt Inven?? ", self.isOpenedBeltWindowWhenClosingInventory
			self.wndBelt.Close()
				
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			self.OnCloseQuestionDialog()
			return
		
		#self.isLoaded = 0
		wndMgr.Hide(self.hWnd)
		
	def Close(self):
		#self.isLoaded = 0
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def Destroy(self):
		self.ClearDictionary()

		self.equipmentTab					= []

		wndEquip							= None
		wndUniqueEquip						= None
		wndDragonSoulButton					= None
		wndMallButton						= None
		wndPremiumPrivateShopButton			= None
		wndCostumeButton					= None

		self.wndEquip						= None
		self.wndUniqueEquip					= None
		self.wndDragonSoulButton			= None
		self.wndMallButton					= None
		self.wndPremiumPrivateShopButton	= None
		self.wndCostumeButton				= None

		wndWikiButton						= None
		wndSwitchbotButton					= None
		self.wndWikiButton					= None
		self.wndSwitchbotButton				= None		
	
		wndOfflineSearchButton2				= None
		wndSwitchBotButton2					= None
		self.wndOfflineSearchButton2		= None
		self.wndSwitchBotButton2			= None
		
		if self.wndBelt:
			self.wndBelt.Destroy()
			self.wndBelt					= None
			
		#Extra variables
		
		self.wndCostume						= None
		self.tooltipItem					= None
		self.interface						= None
		self.questionDialog 				= None

	#Functions of EquipmentWindow
					
	#Function to refactozitation
	def SetEquipmentPage(self, page):
		pass
		#self.equipmentPageIndex = page
		self.equipmentTab[1-page].SetUp()
		self.RefreshEquipSlotWindow()

	def ClickSearchButton(self):
		if self.interface:
			self.interface.OpenPrivateShopSearch(0)
			
	def ClickWikiButton(self):
		if self.interface:
			self.interface.OpenWikiWindow()

	def ClickSwitchButton(self):
		if self.interface:
			self.interface.ToggleSwitchbotWindow()

	def ClickDSSButton(self):
		print "click_dss_button"
		if self.interface:
			self.interface.ToggleDragonSoulWindow()
			
	def ClickCostumeButton(self):
		print "Click Special Button"
		if self.interface:
			self.interface.ToggleSpecialInventoryWindow()

	def ClickOfflineButton(self):
		#if self.interface.wndShopOffline:
		#	if self.interface.wndShopOffline.IsShow() == FALSE or self.interface.wndShopOffline.wBoard[3].IsShow():
		#		self.interface.wndShopOffline.Open()
		#	else:
		#		self.interface.wndShopOffline.Close()
		if self.interface:
			if self.interface.dlgOfflineShopPanel:
				if self.interface.dlgOfflineShopPanel.IsShow():
					self.interface.dlgOfflineShopPanel.CloseReal()
					return
			if self.interface.offlineShopBuilder:
				if self.interface.offlineShopBuilder.IsShow():
					self.interface.offlineShopBuilder.CloseReal()
					return
			net.SendOfflineShopButton()				
	def ClickMallButton(self):
		print "click_mall_button"
		net.SendChatPacket("/click_safebox")

	def RefreshEquipSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndEquip.SetItemSlot
		for i in xrange(player.EQUIPMENT_PAGE_COUNT):
			slotNumber = player.EQUIPMENT_SLOT_START + i
			itemCount = getItemCount(slotNumber)
			if itemCount <= 1:
				itemCount = 0		
			setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)
			if i == 7 or i == 8:
				self.wndInventoryCostume.SetItemSlot(slotNumber, getItemVNum(slotNumber), 0)
			if app.BL_TRANSMUTATION_SYSTEM:
				if not player.GetChangeLookVnum(player.EQUIPMENT, slotNumber) == 0:
					self.wndEquip.SetSlotCoverImage(slotNumber,"icon/item/ingame_convert_Mark.tga")
				else:
					self.wndEquip.EnableSlotCoverImage(slotNumber,False)
					
		if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
			for i in xrange(player.NEW_EQUIPMENT_SLOT_COUNT):
				slotNumber = player.NEW_EQUIPMENT_SLOT_START + i
				itemCount = getItemCount(slotNumber)
				if itemCount <= 1:
					itemCount = 0
				setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)

				print "ENABLE_NEW_EQUIPMENT_SYSTEM", slotNumber, itemCount, getItemVNum(slotNumber)
			if app.ENABLE_PASSIVE_SYSTEM:
				self.wndInventoryTalisman.SetItemSlot(item.PASSIVE_ATTR_SLOT_INDEX_WEAPON, getItemVNum(item.PASSIVE_ATTR_SLOT_INDEX_WEAPON), 0)
				self.wndInventoryTalisman.SetItemSlot(item.PASSIVE_ATTR_SLOT_INDEX_ELEMENT, getItemVNum(item.PASSIVE_ATTR_SLOT_INDEX_ELEMENT), 0)
				self.wndInventoryTalisman.SetItemSlot(item.PASSIVE_ATTR_SLOT_INDEX_ARMOR, getItemVNum(item.PASSIVE_ATTR_SLOT_INDEX_ARMOR), 0)
				self.wndInventoryTalisman.SetItemSlot(item.PASSIVE_ATTR_SLOT_INDEX_ACCE, getItemVNum(item.PASSIVE_ATTR_SLOT_INDEX_ACCE), 0)
				self.wndPassiveItem.SetItemSlot(item.PASSIVE_ATTR_SLOT_INDEX_JOB, getItemVNum(item.PASSIVE_ATTR_SLOT_INDEX_JOB), 0)
				
		self.wndEquip.RefreshSlot()
		self.wndUniqueEquip.RefreshSlot()
		#if self.wndCostume:
		#	self.wndCostume.RefreshCostumeSlot()

	## Slot Event
	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return
		if app.BL_TRANSMUTATION_SYSTEM:
			if player.GetChangeLookWindowOpen() == 1:
				return
		if app.ENABLE_AURA_SYSTEM:
			if player.IsAuraRefineWindowOpen():
				return

		selectedSlotPos = self.__EquipmentLocalSlotPosToGlobalSlotPos(selectedSlotPos)

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()			

			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				#@fixme011 BEGIN (block ds equip)
				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				if player.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
					mouseModule.mouseController.DeattachObject()
					return
				#@fixme011 END

				itemCount = player.GetItemCount(attachedSlotPos)
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				self.__SendMoveItemPacket(attachedSlotPos, selectedSlotPos, attachedCount)
				
			mouseModule.mouseController.DeattachObject()

	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		itemSlotIndex = self.__EquipmentLocalSlotPosToGlobalSlotPos(itemSlotIndex)	

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()
			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				#@fixme011 BEGIN (block ds equip)
				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				if player.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
					mouseModule.mouseController.DeattachObject()
					return
				#@fixme011 END
				self.__DropSrcItemToDestItemInInventory(attachedItemVID, attachedSlotPos, itemSlotIndex)

			mouseModule.mouseController.DeattachObject()

		else:
			curCursorNum = app.GetCursor()
			if app.IsPressed(app.DIK_LCONTROL):
				itemIndex = player.GetItemIndex(itemSlotIndex)

				if True == item.CanAddToQuickSlotItem(itemIndex):
					player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_INVENTORY, itemSlotIndex)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.QUICKSLOT_REGISTER_DISABLE_ITEM)

			else:
				selectedItemVNum = player.GetItemIndex(itemSlotIndex)
				itemCount = player.GetItemCount(itemSlotIndex)
				mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)

				snd.PlaySound("sound/ui/pick.wav")

	def __DropSrcItemToDestItemInEquipment(self, srcItemVID, srcItemSlotPos, dstItemSlotPos):
		if app.ENABLE_AURA_SYSTEM and player.IsAuraRefineWindowOpen():
			return
		if srcItemSlotPos == dstItemSlotPos:
			return
		if app.BL_TRANSMUTATION_SYSTEM:
			if player.GetChangeLookWindowOpen() == 1:
				return
			
		if app.ENABLE_SOULBIND_SYSTEM and item.IsSealScroll(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif item.IsRefineScroll(srcItemVID):
			self.RefineItem(srcItemSlotPos, dstItemSlotPos)
			#self.wndItem.SetUseMode(False)

		elif item.IsMetin(srcItemVID):
			self.AttachMetinToItem(srcItemSlotPos, dstItemSlotPos)

		elif item.IsDetachScroll(srcItemVID):
			self.DetachMetinFromItem(srcItemSlotPos, dstItemSlotPos)

		elif item.IsKey(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif (player.GetItemFlags(srcItemSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif item.GetUseType(srcItemVID) in self.USE_TYPE_TUPLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		else:
			if app.BL_TRANSMUTATION_SYSTEM:
				if item.IsChangeLookClearScroll(srcItemVID):
					if player.CanChangeLookClearItem(srcItemVID, player.INVENTORY, dstItemSlotPos):
						self.__OpenQuestionDialog(srcItemSlotPos, dstItemSlotPos)
						return
						
			if player.IsEquipmentSlot(dstItemSlotPos):

				if item.IsEquipmentVID(srcItemVID):
					self.__UseItem(srcItemSlotPos)

			else:
				self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)

	def OnMoveWindow(self, x, y):
		if self.wndBelt:
			self.wndBelt.AdjustPositionAndSize()
            
	def OverOutItem(self):
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return

		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
		
	def __UseItemQuestionDialog_OnCancel(self):
		self.OnCloseQuestionDialog()

	def __UseItemQuestionDialog_OnAccept(self):
		self.__SendUseItemPacket(self.questionDialog.slotIndex)
		self.OnCloseQuestionDialog()
		
	def __UseItem(self, slotIndex):
		ItemVNum = player.GetItemIndex(slotIndex)
		item.SelectItem(ItemVNum)
		if app.BL_TRANSMUTATION_SYSTEM:
			if player.GetChangeLookWindowOpen() == 1:
				return
		if app.BL_MOVE_COSTUME_ATTR:
			if self.interface.AttachInvenItemToOtherWindowSlot(slotIndex):
				return

		if item.IsFlag(item.ITEM_FLAG_CONFIRM_WHEN_USE):
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM)
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
			self.questionDialog.Open()
			self.questionDialog.slotIndex = slotIndex

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
		else:
			self.__SendUseItemPacket(slotIndex)


	def __CanUseSrcItemToDstItem(self, srcItemVNum, srcSlotPos, dstSlotPos):
		if srcSlotPos == dstSlotPos:
			return False
			
		if item.IsRefineScroll(srcItemVNum):
			if player.REFINE_OK == player.CanRefine(srcItemVNum, dstSlotPos):
				return True
		elif item.IsMetin(srcItemVNum):
			if player.ATTACH_METIN_OK == player.CanAttachMetin(srcItemVNum, dstSlotPos):
				return True
		elif item.IsDetachScroll(srcItemVNum):
			if player.DETACH_METIN_OK == player.CanDetach(srcItemVNum, dstSlotPos):
				return True
		elif item.IsKey(srcItemVNum):
			if player.CanUnlock(srcItemVNum, dstSlotPos):
				return True

		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True
			
		return False
		
	def __SendUseItemPacket(self, slotPos):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemUsePacket(slotPos)

	def __SendMoveItemPacket(self, srcSlotPos, dstSlotPos, srcItemCount):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemMovePacket(srcSlotPos, dstSlotPos, srcItemCount)
		
	def __EquipmentLocalSlotPosToGlobalSlotPos(self, local):
		if player.IsEquipmentSlot(local) or player.IsCostumeSlot(local) or (app.ENABLE_NEW_EQUIPMENT_SYSTEM and player.IsBeltInventorySlot(local)):
			return local

		return self.inventoryPageIndex*player.INVENTORY_PAGE_SIZE + local

	def ShowToolTip(self, slotIndex):
		if None != self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex)
		
	def OverInItem(self, overSlotPos):
		overSlotPosGlobal = self.__EquipmentLocalSlotPosToGlobalSlotPos(overSlotPos)
		
		if mouseModule.mouseController.isAttached():
			attachedItemType = mouseModule.mouseController.GetAttachedType()
			if player.SLOT_TYPE_INVENTORY == attachedItemType:
				
				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()
				
				if attachedItemVNum==player.ITEM_MONEY: # @fixme005
					pass								
				elif self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPosGlobal):
					self.ShowToolTip(overSlotPosGlobal)
					return
		
		self.ShowToolTip(overSlotPosGlobal)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def UseItemSlot(self, slotIndex):		
		curCursorNum = app.GetCursor()
		if app.SELL == curCursorNum:
			return

		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		slotIndex = self.__EquipmentLocalSlotPosToGlobalSlotPos(slotIndex)

		self.__UseItem(slotIndex)
		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def BindInterfaceClass(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)

class InventoryWindow(ui.ScriptWindow):
	liHighlightedItems = []			 

	if app.BL_67_ATTR:
		USE_TYPE_TUPLE = ("USE_CLEAN_SOCKET", "USE_CHANGE_ATTRIBUTE",  "USE_CHANGE_ATTRIBUTE2", "USE_ADD_ATTRIBUTE", "USE_ADD_ATTRIBUTE2", 
						"USE_ADD_ACCESSORY_SOCKET", "USE_PUT_INTO_ACCESSORY_SOCKET", "USE_PUT_INTO_BELT_SOCKET", "USE_PUT_INTO_RING_SOCKET", "USE_CHANGE_COSTUME_ATTR", "USE_RESET_COSTUME_ATTR", "USE_SELECT_ATTRIBUTE")
	else:
		USE_TYPE_TUPLE = ("USE_CLEAN_SOCKET", "USE_CHANGE_ATTRIBUTE",  "USE_ADD_ATTRIBUTE", "USE_ADD_ATTRIBUTE2", "USE_ADD_ACCESSORY_SOCKET", "USE_PUT_INTO_ACCESSORY_SOCKET", 
						"USE_PUT_INTO_BELT_SOCKET", "USE_PUT_INTO_RING_SOCKET", "USE_CHANGE_COSTUME_ATTR", "USE_RESET_COSTUME_ATTR", "USE_SELECT_ATTRIBUTE")	
	if app.ENABLE_AURA_SYSTEM:
		USE_TYPE_TUPLE += ("USE_PUT_INTO_AURA_SOCKET",)
		
	questionDialog = None
	tooltipItem = None
	wndCostume = None
	wndBelt = None
	if app.WJ_ENABLE_TRADABLE_ICON:
		bindWnds = []
	interface = None
	
	dlgPickMoney = None
	sellingSlotNumber = -1
	
	isLoaded = 0
	
	if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
		wndExpandedMoneyBar = None
	#Initialice all objects
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		
		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyBar = None
			self.wndGem = None
		self.inventoryPageIndex = 0
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyBar = None
			self.wndGem = None
	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)

		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyBar:
				self.wndExpandedMoneyBar.Show()

	def BindInterfaceClass(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)

	if app.WJ_ENABLE_TRADABLE_ICON:
		def BindWindow(self, wnd):
			self.bindWnds.append(wnd)
			
	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
		self.isLoaded = 1
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/NewInventory.py")
		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.LoadObject")

		try:
			self.BindObject()
		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.BindObject")

	def BindObject(self):			
		self.wndItem						= self.GetChild("ItemSlot")
		self.wndMoney						= self.GetChild("Money")
		self.wndMoneySlot					= self.GetChild("Money_Slot")
		self.wndSortButton					= self.GetChild("SortButton")
			
		if app.ENABLE_GEM_SYSTEM:
			self.wndGem						= self.GetChild("Gem")
			self.wndGemSlot					= self.GetChild("Gem_Slot")	

		if app.ENABLE_CHEQUE_SYSTEM:
			self.wndCheque					= self.GetChild("Cheque")
			self.wndChequeSlot				= self.GetChild("Cheque_Slot")

			if app.ENABLE_GEM_SYSTEM:
				self.wndMoneyIcon			= self.GetChild("Money_Icon")
				self.wndChequeIcon			= self.GetChild("Cheque_Icon")	
				self.wndGemIcon				= self.GetChild("Gem_Icon")
				height						= self.GetHeight()
				width						= self.GetWidth()

				self.wndMoneyIcon.Hide()
				self.wndMoneySlot.Hide()
				self.wndChequeIcon.Hide()
				self.wndChequeSlot.Hide()
				self.wndGemIcon.Hide()
				self.wndGemSlot.Hide()		
				self.SetSize(width, height - 22)
				self.GetChild("board").SetSize(width, height - 22)

			else:
				self.wndMoneyIcon			= self.GetChild("Money_Icon")
				self.wndChequeIcon			= self.GetChild("Cheque_Icon")
				
				self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 0)
				self.wndChequeIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 1)
				
				self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 0)
				self.wndChequeIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 1)

				self.toolTip = uiToolTip.ToolTip()
				self.toolTip.ClearToolTip()
		else:
			if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
				self.wndMoneyIcon			= self.GetChild("Money_Icon")
				self.wndGemIcon				= self.GetChild("Gem_Icon")
				
				self.wndMoneyIcon.Hide()
				self.wndMoneySlot.Hide()
				self.wndGemIcon.Hide()
				self.wndGemSlot.Hide()
					
				height = self.GetHeight()
				width = self.GetWidth()
				self.SetSize(width, height - 22)
				self.GetChild("board").SetSize(width, height - 22)
			else:
				self.wndMoneyIcon			= self.GetChild("Money_Icon")
				
				self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 0)
				self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 0)
				self.toolTip = uiToolTip.ToolTip()
				self.toolTip.ClearToolTip()

		self.inventoryTab			= []
		for i in xrange(player.INVENTORY_PAGE_COUNT):
			self.inventoryTab.append(self.GetChild("Inventory_Tab_%02d" % (i+1)))			

		if app.BL_TRANSMUTATION_SYSTEM:
			self.dlgQuestion = uiCommon.QuestionDialog2()
			self.dlgQuestion.Close()
			self.listHighlightedChangeLookSlot = []

				
		self.BindEvent()
		
	def BindEvent(self):
		## Item
		self.wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		self.wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		self.wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		self.wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		self.wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		## PickMoneyDialog
		dlgPickMoney = uiPickMoney.PickMoneyDialog()
		dlgPickMoney.LoadDialog()
		dlgPickMoney.Hide()

		## RefineDialog
		self.refineDialog = uiRefine.RefineDialog()
		self.refineDialog.Hide()

		## AttachMetinDialog
		if app.WJ_ENABLE_TRADABLE_ICON:  
			self.attachMetinDialog = uiAttachMetin.AttachMetinDialog(self)
			self.BindWindow(self.attachMetinDialog)
		else:
			self.attachMetinDialog = uiAttachMetin.AttachMetinDialog()
		self.attachMetinDialog.Hide()

		## MoneySlot
		self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))

		self.wndSortButton.SetEvent(self.OnSortInventory)
					
		for i in xrange(player.INVENTORY_PAGE_COUNT):
			self.inventoryTab[i].SetEvent(lambda arg=i: self.SetInventoryPage(arg))
		self.inventoryTab[0].Down()

		self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
		
		self.dlgPickMoney = dlgPickMoney

		## Refresh
		self.SetInventoryPage(0)
		self.RefreshItemSlot()
		self.RefreshStatus()		
	#Destroy and close all objects

	def Hide(self):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			self.OnCloseQuestionDialog()
			return
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		if self.dlgPickMoney:
			self.dlgPickMoney.Close()
			
		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyBar:
				self.wndExpandedMoneyBar.Close()
		
		#self.isLoaded = 0
		wndMgr.Hide(self.hWnd)
		
	def Destroy(self):
		self.ClearDictionary()

		self.dlgPickMoney.Destroy()
		self.dlgPickMoney = 0

		self.refineDialog.Destroy()
		self.refineDialog = 0

		self.attachMetinDialog.Destroy()
		self.attachMetinDialog = 0

		self.tooltipItem = None
		self.wndItem = 0
		self.dlgPickMoney = 0
		self.wndMoney = 0
		self.wndMoneySlot = 0
		if app.ENABLE_GEM_SYSTEM:
			self.wndGem = 0
			self.wndGemSlot = 0
		self.questionDialog = None
		self.interface = None
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.bindWnds = []
				
		if app.BL_TRANSMUTATION_SYSTEM:
			self.dlgQuestion = None

		self.inventoryTab = []
		
		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyBar = None
			
	def Close(self):
		self.Hide()
		
	#Functions of InventoryWindow	
	
	def OnSortInventory(self):
		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText(localeInfo.INVENTORY_SORT_QUESTION)
		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.AcceptSortInventory))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.CancelSortInventory))
		self.questionDialog.Open()
		self.questionDialog.inventoryTypeIndex = self.inventoryTypeIndex

	def CancelSortInventory(self):
		self.OnCloseQuestionDialog()

	def AcceptSortInventory(self):
		if self.questionDialog:
			net.SendChatPacket("/sort_inventory")
			self.questionDialog.Close()
		self.questionDialog = None
		
	if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
		def OverInToolTip(self, arg) :	
			arglen = len(str(arg))
			pos_x, pos_y = wndMgr.GetMousePosition()
			
			self.toolTip.ClearToolTip()
			self.toolTip.SetToolTipPosition(pos_x + 5, pos_y - 5)
			self.toolTip.AppendTextLine(arg, 0xffffff00)
			self.toolTip.Show()
		
		def OverOutToolTip(self) :
			self.toolTip.Hide()
			
		def EventProgress(self, event_type, idx) :
			if "mouse_over_in" == str(event_type) :
				if idx == 0 :
					self.OverInToolTip(localeInfo.CHEQUE_SYSTEM_UNIT_YANG)
				elif idx == 1 :
					self.OverInToolTip(localeInfo.CHEQUE_SYSTEM_UNIT_WON)
				elif app.ENABLE_GEM_SYSTEM and idx == 2 :
					self.OverInToolTip(localeInfo.GEM_SYSTEM_NAME)
				else:
					return 
			elif "mouse_over_out" == str(event_type) :
				self.OverOutToolTip()
			else:
				return
		def SetExpandedMoneyBar(self, wndBar):
			self.wndExpandedMoneyBar = wndBar
			if self.wndExpandedMoneyBar:
				self.wndMoneySlot = self.wndExpandedMoneyBar.GetMoneySlot()
				self.wndMoney = self.wndExpandedMoneyBar.GetMoney()
				if app.ENABLE_CHEQUE_SYSTEM:
					## ? ??
					self.wndMoneyIcon = self.wndExpandedMoneyBar.GetMoneyIcon()
					if self.wndMoneyIcon:
						self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 0)
						self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 0)
					if self.wndMoneySlot:
						self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog), 0)
					## 2??? ??
					self.wndChequeIcon = self.wndExpandedMoneyBar.GetChequeIcon()
					if self.wndChequeIcon:
						self.wndChequeIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 1)
						self.wndChequeIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 1)
					self.wndChequeSlot = self.wndExpandedMoneyBar.GetChequeSlot() 
					if self.wndChequeSlot:
						self.wndChequeSlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog), 1)
					self.wndCheque = self.wndExpandedMoneyBar.GetCheque()
					## ?? ??
					self.wndGemIcon = self.wndExpandedMoneyBar.GetGemIcon()
					if self.wndGemIcon:
						self.wndGemIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 2)
						self.wndGemIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 2)
					self.wndGem = self.wndExpandedMoneyBar.GetGem()
					self.toolTip = uiToolTip.ToolTip()
					self.toolTip.ClearToolTip()
				else:
					if self.wndMoneySlot:
						self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))
					if app.ENABLE_GEM_SYSTEM:
						self.wndGem = self.wndExpandedMoneyBar.GetGem()
						self.wndGemSlot = self.wndExpandedMoneyBar.GetGemSlot()
						
	def SetInventoryPage(self, page):
		self.inventoryPageIndex = page
		for i in xrange(player.INVENTORY_PAGE_COUNT):
			if i!=page:
				self.inventoryTab[i].SetUp()
				
		self.RefreshBagSlotWindow()
			
			
	#RunMouseWheel
	def OnMouseWheel(self, nLen):
		if nLen > 0:
			self.inventoryPageIndex += 1
			if self.inventoryPageIndex > 3:
				self.inventoryPageIndex = 3
				
			for i in xrange(4):
				if i != self.inventoryPageIndex:
					self.inventoryTab[i].SetUp()

			self.inventoryTab[self.inventoryPageIndex].Down()
			self.RefreshBagSlotWindow()
		else:
			self.inventoryPageIndex -= 1
			
			if self.inventoryPageIndex < 0:
				self.inventoryPageIndex = 0

			for i in xrange(4):
				if i != self.inventoryPageIndex:
					self.inventoryTab[i].SetUp()

			self.inventoryTab[self.inventoryPageIndex].Down()
			self.RefreshBagSlotWindow()
								
	def OpenPickMoneyDialog(self):

		if mouseModule.mouseController.isAttached():

			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			if player.SLOT_TYPE_SAFEBOX == mouseModule.mouseController.GetAttachedType():

				if player.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

			mouseModule.mouseController.DeattachObject()

		else:
			curMoney = player.GetElk()

			if curMoney <= 0:
				return

			self.dlgPickMoney.SetTitleName(localeInfo.PICK_MONEY_TITLE)
			self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickMoney))
			self.dlgPickMoney.Open(curMoney)
			self.dlgPickMoney.SetMax(9)
			
	def OnPickMoney(self, money):
		mouseModule.mouseController.AttachMoney(self, player.SLOT_TYPE_INVENTORY, money)

	def OnPickItem(self, count):
		itemSlotIndex = self.dlgPickMoney.itemGlobalSlotIndex

		selectedItemVNum = player.GetItemIndex(itemSlotIndex)
		mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, count)

	def __InventoryLocalSlotPosToGlobalSlotPos(self, local):
		if player.IsEquipmentSlot(local) or player.IsCostumeSlot(local) or (app.ENABLE_NEW_EQUIPMENT_SYSTEM and player.IsBeltInventorySlot(local)):
			return local

		return self.inventoryPageIndex*player.INVENTORY_PAGE_SIZE + local

	def GetInventoryPageIndex(self):
		return self.inventoryPageIndex								 
	if app.WJ_ENABLE_TRADABLE_ICON:
		def RefreshMarkSlots(self, localIndex=None):
			if not self.interface:
				return

			onTopWnd = self.interface.GetOnTopWindow()
			if localIndex:
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(localIndex)
					
				if onTopWnd == player.ON_TOP_WND_NONE:
					self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_SHOP:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SELL):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_EXCHANGE:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_GIVE):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_PRIVATE_SHOP:
					if player.IsAntiFlagBySlot(slotNumber, item.ITEM_ANTIFLAG_MYSHOP):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_SAFEBOX:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SAFEBOX):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif app.BL_MOVE_COSTUME_ATTR and onTopWnd == player.ON_TOP_WND_ITEM_COMB:
					if self.interface.MarkUnusableInvenSlotMoveCostumeAttr(onTopWnd, slotNumber):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)
						
				elif app.BL_67_ATTR and onTopWnd == player.ON_TOP_WND_ATTR_67:
					mark = (not self.interface.IsAttr67RegistItem() and not uiAttr67Add.Attr67AddWindow.CantAttachToAttrSlot(slotNumber, True)) or \
						(self.interface.IsAttr67RegistItem() and not self.interface.IsAttr67SupportItem() and not uiAttr67Add.Attr67AddWindow.IsSupportItem(slotNumber))

					if mark:
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)
				return

			for i in xrange(player.INVENTORY_PAGE_SIZE):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)	
						
				if onTopWnd == player.ON_TOP_WND_NONE:
					self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_SHOP:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SELL):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_EXCHANGE:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_GIVE):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_PRIVATE_SHOP:
					if player.IsAntiFlagBySlot(slotNumber, item.ITEM_ANTIFLAG_MYSHOP):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_SAFEBOX:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SAFEBOX):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)
				elif app.BL_MOVE_COSTUME_ATTR and onTopWnd == player.ON_TOP_WND_ITEM_COMB:
					if self.interface.MarkUnusableInvenSlotMoveCostumeAttr(onTopWnd, slotNumber):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)
				elif app.BL_67_ATTR and onTopWnd == player.ON_TOP_WND_ATTR_67:
					mark = (not self.interface.IsAttr67RegistItem() and not uiAttr67Add.Attr67AddWindow.CantAttachToAttrSlot(slotNumber, True)) or \
						(self.interface.IsAttr67RegistItem() and not self.interface.IsAttr67SupportItem() and not uiAttr67Add.Attr67AddWindow.IsSupportItem(slotNumber))
                    
					if mark:
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)
						
	def RefreshBagSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndItem.SetItemSlot

		for i in xrange(player.INVENTORY_PAGE_SIZE):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

			itemCount = getItemCount(slotNumber)
			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0

			itemVnum = getItemVNum(slotNumber)
			setItemVNum(i, itemVnum, itemCount)

			if itemVnum == 0 and slotNumber in self.liHighlightedItems:
				self.liHightlightedItems.remove(slotNumber)
				
			if constInfo.IS_AUTO_POTION(itemVnum):
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]

				isActivated = 0 != metinSocket[0]

				if isActivated:
					self.wndItem.ActivateSlot(i)
					potionType = 0;
					if constInfo.IS_AUTO_POTION_HP(itemVnum):
						potionType = player.AUTO_POTION_TYPE_HP
					elif constInfo.IS_AUTO_POTION_SP(itemVnum):
						potionType = player.AUTO_POTION_TYPE_SP

					usedAmount = int(metinSocket[1])
					totalAmount = int(metinSocket[2])
					player.SetAutoPotionInfo(potionType, isActivated, (totalAmount - usedAmount), totalAmount, self.__InventoryLocalSlotPosToGlobalSlotPos(i))
				else:
					self.wndItem.DeactivateSlot(i)
					
			elif constInfo.IS_ACCE_ITEM(itemVnum, 1) == TRUE:
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]
				isActivated = metinSocket[0]
				if isActivated == 1:
					player.SetAcceInfo(isActivated, i)
					self.wndItem.ActivateAcceSlot(i)
				else:
					self.wndItem.DeactivateAcceSlot(i)

			elif itemVnum >= 53001 and itemVnum <= 53256:
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]
				isActivated = metinSocket[2]
				if isActivated:
					self.wndItem.ActivateSlot(i)
				else:
					self.wndItem.DeactivateSlot(i)

			elif itemVnum >= 55701 and itemVnum <= 55712:
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]
				isActivated = metinSocket[2]
				if isActivated:
					self.wndItem.ActivateSlot(i)
				else:
					self.wndItem.DeactivateSlot(i)

			elif (itemVnum >= 71270 and itemVnum <= 71297) or itemVnum == 76018 or itemVnum == 76012:
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]
				isActivated = metinSocket[2]
				if isActivated == 1:
					self.wndItem.ActivateSlot(i)
				else:
					self.wndItem.DeactivateSlot(i)

			if app.WJ_ENABLE_TRADABLE_ICON:
				self.RefreshMarkSlots(i)	
			else:
				self.wndItem.DeactivateSlot(slotNumber)

		self.__RefreshHighlights()

		self.wndItem.RefreshSlot()
				
		if self.wndBelt:
			self.wndBelt.RefreshSlot()

		if app.BL_TRANSMUTATION_SYSTEM:
			if not player.GetChangeLookVnum(player.INVENTORY, slotNumber) == 0:
				self.wndItem.SetSlotCoverImage(i,"icon/item/ingame_convert_Mark.tga")
			else:
				self.wndItem.EnableSlotCoverImage(i,False)
			self.__HighlightSlot_Refresh()
			
		if app.WJ_ENABLE_TRADABLE_ICON:
			map(lambda wnd:wnd.RefreshLockedSlot(), self.bindWnds)
			
	def RefreshItemSlot(self):
		self.RefreshBagSlotWindow()
			
	def RefreshStatus(self):
		money = player.GetElk()
		self.wndMoney.SetText(localeInfo.NumberToMoneyString(money))
		if app.ENABLE_GEM_SYSTEM:
			gem = player.GetGem()
			self.wndGem.SetText(localeInfo.NumberToGemString(gem))
			
	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	if app.BL_TRANSMUTATION_SYSTEM:
		def IsDlgQuestionShow(self):
			if self.dlgQuestion.IsShow():
				return True
			else:
				return False
		
		def CancelDlgQuestion(self):
			self.__Cancel()
		
		def __OpenQuestionDialog(self, srcItemPos, dstItemPos):
			if self.interface.IsShowDlgQuestionWindow():
				self.interface.CloseDlgQuestionWindow()
				
			getItemVNum=player.GetItemIndex
			self.srcItemPos = srcItemPos
			self.dstItemPos = dstItemPos
			
			self.dlgQuestion.SetAcceptEvent(ui.__mem_func__(self.__Accept))
			self.dlgQuestion.SetCancelEvent(ui.__mem_func__(self.__Cancel))

			self.dlgQuestion.SetText1("%s" % item.GetItemName(getItemVNum(srcItemPos)) )
			self.dlgQuestion.SetText2(localeInfo.INVENTORY_REALLY_USE_ITEM)

			self.dlgQuestion.Open()
			
		def __Accept(self):
			self.dlgQuestion.Close()
			self.__SendUseItemToItemPacket(self.srcItemPos, self.dstItemPos)
			self.srcItemPos = (0, 0)
			self.dstItemPos = (0, 0)

		def __Cancel(self):
			self.srcItemPos = (0, 0)
			self.dstItemPos = (0, 0)
			self.dlgQuestion.Close()
			
	def SellItem(self):
		if self.sellingSlotitemIndex == player.GetItemIndex(self.sellingSlotNumber):
			if self.sellingSlotitemCount == player.GetItemCount(self.sellingSlotNumber):
				net.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, player.INVENTORY)
				snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()
		
	def OnDetachMetinFromItem(self):
		if None == self.questionDialog:
			return

		#net.SendItemUseToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
		self.__SendUseItemToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return

		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
		
	## Slot Event
	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return
		if app.BL_TRANSMUTATION_SYSTEM:
			if player.GetChangeLookWindowOpen() == 1:
				return
		if app.ENABLE_AURA_SYSTEM:
			if player.IsAuraRefineWindowOpen():
				return
				
		selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos)

		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
			
			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				#@fixme011 BEGIN (block ds equip)
				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				if player.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
					mouseModule.mouseController.DeattachObject()
					return
				#@fixme011 END

				itemCount = player.GetItemCount(attachedSlotPos)
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				self.__SendMoveItemPacket(attachedSlotPos, selectedSlotPos, attachedCount)

				if item.IsRefineScroll(attachedItemIndex):
					self.wndItem.SetUseMode(False)

			elif app.ENABLE_SWITCHBOT and player.SLOT_TYPE_SWITCHBOT == attachedSlotType:
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				net.SendItemMovePacket(player.SWITCHBOT, attachedSlotPos, player.INVENTORY, selectedSlotPos, attachedCount)

			elif player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				mouseModule.mouseController.RunCallBack("INVENTORY")

			elif player.SLOT_TYPE_SHOP == attachedSlotType:
				net.SendShopBuyPacket(attachedSlotPos)

			elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:

				if player.ITEM_MONEY == attachedItemIndex:
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

				else:
					net.SendSafeboxCheckoutPacket(attachedSlotPos, selectedSlotPos)

			elif player.SLOT_TYPE_MALL == attachedSlotType:
				net.SendMallCheckoutPacket(attachedSlotPos, selectedSlotPos)

			elif app.ENABLE_AURA_SYSTEM and player.SLOT_TYPE_AURA == attachedSlotType:
				net.SendAuraRefineCheckOut(attachedSlotPos, player.GetAuraRefineWindowType())
				
			mouseModule.mouseController.DeattachObject()
			
			
	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex)	

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()

			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				#@fixme011 BEGIN (block ds equip)
				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				if player.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
					mouseModule.mouseController.DeattachObject()
					return
				#@fixme011 END
				self.__DropSrcItemToDestItemInInventory(attachedItemVID, attachedSlotPos, itemSlotIndex)

			mouseModule.mouseController.DeattachObject()

		else:
			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)

			elif app.BUY == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)

			elif app.IsPressed(app.DIK_LALT):
				link = player.GetItemLink(itemSlotIndex)
				ime.PasteString(link)

			elif app.IsPressed(app.DIK_LSHIFT):
				itemCount = player.GetItemCount(itemSlotIndex)

				if itemCount > 1:
					self.dlgPickMoney.SetTitleName(localeInfo.PICK_ITEM_TITLE)
					self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
					self.dlgPickMoney.Open(itemCount)
					self.dlgPickMoney.itemGlobalSlotIndex = itemSlotIndex
			elif app.IsPressed(app.DIK_LCONTROL):
				itemIndex = player.GetItemIndex(itemSlotIndex)

				if True == item.CanAddToQuickSlotItem(itemIndex):
					player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_INVENTORY, itemSlotIndex)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.QUICKSLOT_REGISTER_DISABLE_ITEM)

			else:
				selectedItemVNum = player.GetItemIndex(itemSlotIndex)
				itemCount = player.GetItemCount(itemSlotIndex)
				mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)

				if self.__IsUsableItemToItem(selectedItemVNum, itemSlotIndex):
					self.wndItem.SetUseMode(True)
				else:
					self.wndItem.SetUseMode(False)

				snd.PlaySound("sound/ui/pick.wav")

	def UseTransportBox(self):
		self.__SendUseItemToItemPacket(self.questionDialog.src, self.questionDialog.dst)
		self.OnCloseQuestionDialog()
	
	def UseProtein(self):
		self.__SendUseItemToItemPacket(self.questionDialog.src, self.questionDialog.dst)
		self.OnCloseQuestionDialog()
			
	def __DropSrcItemToDestItemInInventory(self, srcItemVID, srcItemSlotPos, dstItemSlotPos):
		if app.ENABLE_AURA_SYSTEM and player.IsAuraRefineWindowOpen():
			return
		if srcItemSlotPos == dstItemSlotPos:
			return
		if app.BL_TRANSMUTATION_SYSTEM:
			if player.GetChangeLookWindowOpen() == 1:
				return

		if srcItemVID == 100003:
			item.SelectItem(player.GetItemIndex(dstItemSlotPos))
			if item.ITEM_TYPE_COSTUME:
				self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
		
		if srcItemVID >= 55701 and srcItemVID <= 55711 and player.GetItemIndex(dstItemSlotPos) == 55002:
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText("¢¯Quieres agregar a tu acompanante a la caja de transporte?")
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.UseTransportBox))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.src = srcItemSlotPos
			self.questionDialog.dst = dstItemSlotPos
			
		if srcItemVID == 55001 and player.GetItemIndex(dstItemSlotPos) >= 55701 and player.GetItemIndex(dstItemSlotPos) <= 55711:
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText("¢¯Quieres alimentar a tu acompanante?")
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.UseProtein))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.src = srcItemSlotPos
			self.questionDialog.dst = dstItemSlotPos
			
		if app.ENABLE_SOULBIND_SYSTEM and item.IsSealScroll(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif item.IsRefineScroll(srcItemVID):
			self.RefineItem(srcItemSlotPos, dstItemSlotPos)
			self.wndItem.SetUseMode(False)

		elif item.IsMetin(srcItemVID):
			self.AttachMetinToItem(srcItemSlotPos, dstItemSlotPos)

		elif item.IsDetachScroll(srcItemVID):
			self.DetachMetinFromItem(srcItemSlotPos, dstItemSlotPos)

		elif item.IsKey(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif (player.GetItemFlags(srcItemSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif item.GetUseType(srcItemVID) in self.USE_TYPE_TUPLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		else:
			if app.BL_TRANSMUTATION_SYSTEM:
				if item.IsChangeLookClearScroll(srcItemVID):
					if player.CanChangeLookClearItem(srcItemVID, player.INVENTORY, dstItemSlotPos):
						self.__OpenQuestionDialog(srcItemSlotPos, dstItemSlotPos)
						return
						
			if player.IsEquipmentSlot(dstItemSlotPos):
				if item.IsEquipmentVID(srcItemVID):
					self.__UseItem(srcItemSlotPos)

			else:
				self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
				
	def __SellItem(self, itemSlotPos):		
		
		if not player.IsEquipmentSlot(itemSlotPos):
			self.sellingSlotNumber = itemSlotPos
			itemIndex = player.GetItemIndex(itemSlotPos)
			itemCount = player.GetItemCount(itemSlotPos)


			self.sellingSlotitemIndex = itemIndex
			self.sellingSlotitemCount = itemCount

			item.SelectItem(itemIndex)
			if item.IsAntiFlag(item.ANTIFLAG_SELL):
				popup = uiCommon.PopupDialog()
				popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
				popup.SetAcceptEvent(self.__OnClosePopupDialog)
				popup.Open()
				self.popup = popup
				return

			itemPrice = item.GetISellItemPrice()

			if item.Is1GoldItem():
				itemPrice = itemCount / itemPrice / 1
			else:
				itemPrice = itemPrice * itemCount / 1

			item.GetItemName(itemIndex)
			itemName = item.GetItemName()

			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, itemCount, itemPrice))
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.count = itemCount

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
			
	def __OnClosePopupDialog(self):
		self.pop = None

	def RefineItem(self, scrollSlotPos, targetSlotPos):		


		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		if player.REFINE_OK != player.CanRefine(scrollIndex, targetSlotPos):
			return
		if app.ENABLE_REFINE_RENEWAL:
			constInfo.AUTO_REFINE_TYPE = 1
			constInfo.AUTO_REFINE_DATA["ITEM"][0] = scrollSlotPos
			constInfo.AUTO_REFINE_DATA["ITEM"][1] = targetSlotPos
		self.__SendUseItemToItemPacket(scrollSlotPos, targetSlotPos)
		return
		
		result = player.CanRefine(scrollIndex, targetSlotPos)

		if player.REFINE_ALREADY_MAX_SOCKET_COUNT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_MORE_SOCKET)

		elif player.REFINE_NEED_MORE_GOOD_SCROLL == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NEED_BETTER_SCROLL)

		elif player.REFINE_CANT_MAKE_SOCKET_ITEM == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_SOCKET_DISABLE_ITEM)

		elif player.REFINE_NOT_NEXT_GRADE_ITEM == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_UPGRADE_DISABLE_ITEM)

		elif player.REFINE_CANT_REFINE_METIN_TO_EQUIPMENT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)

		if player.REFINE_OK != result:
			return

		self.refineDialog.Open(scrollSlotPos, targetSlotPos)
		
	def DetachMetinFromItem(self, scrollSlotPos, targetSlotPos):
		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		if constInfo.IS_ACCE_ITEM_DETACH(scrollIndex) == TRUE:
			item.SelectItem(targetIndex)
			if item.GetItemSubType() == item.COSTUME_TYPE_ACCE:
				if self.GetAcceAttribute(targetSlotPos) == 0:
					return
				
				self.questionDialog = uiCommon.QuestionDialog()
				self.questionDialog.SetText(localeInfo.ACCE_DO_YOU_REMOVE_ATTR)
				self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnDetachMetinFromItem))
				self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
				self.questionDialog.Open()
				self.questionDialog.sourcePos = scrollSlotPos
				self.questionDialog.targetPos = targetSlotPos
			else:
				return
		else:
			if not player.CanDetach(scrollIndex, targetSlotPos):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
				return

			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.REFINE_DO_YOU_SEPARATE_METIN)
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnDetachMetinFromItem))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.sourcePos = scrollSlotPos
			self.questionDialog.targetPos = targetSlotPos

	def AttachMetinToItem(self, metinSlotPos, targetSlotPos):
		metinIndex = player.GetItemIndex(metinSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		item.SelectItem(metinIndex)
		itemName = item.GetItemName()

		result = player.CanAttachMetin(metinIndex, targetSlotPos)

		if player.ATTACH_METIN_NOT_MATCHABLE_ITEM == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_CAN_NOT_ATTACH(itemName))

		if player.ATTACH_METIN_NO_MATCHABLE_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_SOCKET(itemName))

		elif player.ATTACH_METIN_NOT_EXIST_GOLD_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_GOLD_SOCKET(itemName))

		elif player.ATTACH_METIN_CANT_ATTACH_TO_EQUIPMENT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)

		if player.ATTACH_METIN_OK != result:
			return

		self.attachMetinDialog.Open(metinSlotPos, targetSlotPos)
		
	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()
		
	def OverInItem(self, overSlotPos):
		overSlotPosGlobal = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)
		self.wndItem.SetUsableItem(False)
		
		if overSlotPosGlobal in self.liHighlightedItems:
			self.liHighlightedItems.remove(overSlotPosGlobal)
			self.wndItem.DeactivateSlot(overSlotPos)
		
		if mouseModule.mouseController.isAttached():
			attachedItemType = mouseModule.mouseController.GetAttachedType()
			if player.SLOT_TYPE_INVENTORY == attachedItemType:
				
				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()
				
				if attachedItemVNum==player.ITEM_MONEY: # @fixme005
					pass								
				elif self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPosGlobal):
					self.wndItem.SetUsableItem(True)
					self.ShowToolTip(overSlotPosGlobal)
					return
		
		self.ShowToolTip(overSlotPosGlobal)
		
	def __IsUsableItemToItem(self, srcItemVNum, srcSlotPos):
		if srcItemVNum >= 55701 and srcItemVNum <= 55711:
			return True
		
		if srcItemVNum == 55001:
			return True

		item.SelectItem(player.GetItemIndex(srcItemVNum))
		if item.ITEM_TYPE_COSTUME and (item.COSTUME_TYPE_WEAPON or item.COSTUME_TYPE_BODY or item.COSTUME_TYPE_HAIR):
			return True
				
		if item.IsRefineScroll(srcItemVNum):
			return True
		elif item.IsMetin(srcItemVNum):
			return True
		elif item.IsDetachScroll(srcItemVNum):
			return True
		elif item.IsKey(srcItemVNum):
			return True
		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True
		else:
			if app.BL_TRANSMUTATION_SYSTEM:
				if item.IsChangeLookClearScroll(srcItemVNum):
					return True
			if item.GetUseType(srcItemVNum) in self.USE_TYPE_TUPLE:
				return True

		return False

	def __CanUseSrcItemToDstItem(self, srcItemVNum, srcSlotPos, dstSlotPos):
		if srcSlotPos == dstSlotPos:
			return False
			
		if srcItemVNum == 100003:
			item.SelectItem(player.GetItemIndex(dstSlotPos))
			if item.ITEM_TYPE_COSTUME and (item.COSTUME_TYPE_WEAPON or item.COSTUME_TYPE_BODY or item.COSTUME_TYPE_HAIR):
				return True
				
		if srcItemVNum >= 55701 and  srcItemVNum <= 55711 and player.GetItemIndex(dstSlotPos) == 55002:			
			return True		
		
		if srcItemVNum == 55001 and player.GetItemIndex(dstSlotPos) >= 55701 and player.GetItemIndex(dstSlotPos) <= 55711:			
			return True
			
		if item.IsRefineScroll(srcItemVNum):
			if player.REFINE_OK == player.CanRefine(srcItemVNum, dstSlotPos):
				return True
		elif item.IsMetin(srcItemVNum):
			if player.ATTACH_METIN_OK == player.CanAttachMetin(srcItemVNum, dstSlotPos):
				return True
		elif item.IsDetachScroll(srcItemVNum):
			if player.DETACH_METIN_OK == player.CanDetach(srcItemVNum, dstSlotPos):
				return True
		elif item.IsKey(srcItemVNum):
			if player.CanUnlock(srcItemVNum, dstSlotPos):
				return True

		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True

		else:
			if app.BL_TRANSMUTATION_SYSTEM:
				if player.CanChangeLookClearItem(srcItemVNum, player.INVENTORY, dstSlotPos):
					return True
			useType=item.GetUseType(srcItemVNum)
			if "USE_CLEAN_SOCKET" == useType:
				if self.__CanCleanBrokenMetinStone(dstSlotPos):
					return True
			elif "USE_CHANGE_ATTRIBUTE" == useType:
				if self.__CanChangeItemAttrList(dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE2" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			elif "USE_ADD_ACCESSORY_SOCKET" == useType:
				if self.__CanAddAccessorySocket(dstSlotPos):
					return True
			elif "USE_PUT_INTO_ACCESSORY_SOCKET" == useType:
				if self.__CanPutAccessorySocket(dstSlotPos, srcItemVNum):
					return True
			elif "USE_PUT_INTO_BELT_SOCKET" == useType:
				dstItemVNum = player.GetItemIndex(dstSlotPos)
				print "USE_PUT_INTO_BELT_SOCKET", srcItemVNum, dstItemVNum

				item.SelectItem(dstItemVNum)

				if item.ITEM_TYPE_BELT == item.GetItemType():
					return True
			elif "USE_CHANGE_COSTUME_ATTR" == useType:
				if self.__CanChangeCostumeAttrList(dstSlotPos):
					return True
			elif "USE_RESET_COSTUME_ATTR" == useType:
				if self.__CanResetCostumeAttr(dstSlotPos):
					return True
			elif app.BL_67_ATTR and "USE_CHANGE_ATTRIBUTE2" == useType:
				if self.__CanChangeItemAttrList2(dstSlotPos):
					return True
			if app.ENABLE_AURA_SYSTEM:
				if "USE_PUT_INTO_AURA_SOCKET" == useType:
					if app.ENABLE_EXTEND_INVEN_SYSTEM:
						if mouseModule.mouseController.isAttached():
							attachedSlotType = mouseModule.mouseController.GetAttachedType()
							dstSlotWindow = player.SlotTypeToInvenType(attachedSlotType)
						if item.ITEM_TYPE_COSTUME == player.GetItemTypeBySlot(dstSlotWindow, dstSlotPos) and item.COSTUME_TYPE_AURA == player.GetItemSubTypeBySlot(dstSlotWindow, dstSlotPos):
							if player.GetItemMetinSocket(dstSlotWindow, dstSlotPos, player.ITEM_SOCKET_AURA_BOOST) == 0:
								return True
					else:
						dstItemVnum = player.GetItemIndex(dstSlotPos)
						item.SelectItem(dstItemVnum)
						if item.ITEM_TYPE_COSTUME == item.GetItemType() and item.COSTUME_TYPE_AURA == item.GetItemSubType():
							if player.GetItemMetinSocket(dstSlotPos, player.ITEM_SOCKET_AURA_BOOST) == 0:
								return True
			elif app.BL_MOVE_COSTUME_ATTR and "USE_CHANGE_COSTUME_ATTR" == useType:
				if self.__CanChangeCostumeAttrList(dstSlotPos):
					return True
			elif app.BL_MOVE_COSTUME_ATTR and "USE_RESET_COSTUME_ATTR" == useType:
				if self.__CanResetCostumeAttr(dstSlotPos):
					return True
			elif app.BL_CHANGED_ATTR and "USE_SELECT_ATTRIBUTE" == useType:
				if self.__CanChangeItemAttrList(dstSlotPos):
					return True
		return False
		
	def __CanCleanBrokenMetinStone(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.ITEM_TYPE_WEAPON != item.GetItemType():
			return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemMetinSocket(dstSlotPos, i) == constInfo.ERROR_METIN_STONE:
				return True

		return False

	def __CanChangeItemAttrList(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
			return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				return True

		return False

	if app.BL_67_ATTR:
		def __CanChangeItemAttrList2(self, dstSlotPos):
			return uiAttr67Add.Attr67AddWindow.CantAttachToAttrSlot(dstSlotPos, False)
			
	def __CanChangeCostumeAttrList(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_COSTUME:
			return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				return True

		return False

	def __CanResetCostumeAttr(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_COSTUME:
			return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				return True

		return False

	def __CanPutAccessorySocket(self, dstSlotPos, mtrlVnum):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)

		if mtrlVnum != constInfo.GET_ACCESSORY_MATERIAL_VNUM(dstItemVNum, item.GetItemSubType()):
			return False

		if curCount>=maxCount:
			return False

		return True

	def __CanAddAccessorySocket(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)

		ACCESSORY_SOCKET_MAX_SIZE = 3
		if maxCount >= ACCESSORY_SOCKET_MAX_SIZE:
			return False

		return True

	def __CanAddItemAttr(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
			return False

		attrCount = 0
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				attrCount += 1

		if attrCount<4:
			return True

		return False

	def ShowToolTip(self, slotIndex):
		if None != self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex)
				
	if app.BL_MOVE_COSTUME_ATTR:
		def __CanChangeCostumeAttrList(self, dstSlotPos):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False
			
			item.SelectItem(dstItemVNum)
			
			if item.GetItemType() !=item.ITEM_TYPE_COSTUME:	 
				return False

			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				type, value = player.GetItemAttribute(dstSlotPos, i)
				if type != 0:
					return True
			
			return False
		
		def __CanResetCostumeAttr(self, dstSlotPos):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False
			
			item.SelectItem(dstItemVNum)
			
			if item.GetItemType() !=item.ITEM_TYPE_COSTUME:	 	  
				return False
			
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				type, value = player.GetItemAttribute(dstSlotPos, i)
				if type != 0:
					return True
			
			return False
			
	def OnTop(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetTop()
		if app.WJ_ENABLE_TRADABLE_ICON:
			map(lambda wnd:wnd.RefreshLockedSlot(), self.bindWnds)
			self.RefreshMarkSlots()
			
	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def UseItemSlot(self, slotIndex):				
		
		curCursorNum = app.GetCursor()
		if app.SELL == curCursorNum:
			return

		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			if self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.AutoSetItem((player.INVENTORY, slotIndex), 1)
				return

		self.__UseItem(slotIndex)
		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()

	def __UseItem(self, slotIndex):
		if app.ENABLE_AURA_SYSTEM:
			if player.IsAuraRefineWindowOpen():
				self.__UseItemAura(slotIndex)
				return
		ItemVNum = player.GetItemIndex(slotIndex)
		item.SelectItem(ItemVNum)
		if app.BL_TRANSMUTATION_SYSTEM:
			if player.GetChangeLookWindowOpen() == 1:
				return
		if app.BL_MOVE_COSTUME_ATTR:
			if self.interface.AttachInvenItemToOtherWindowSlot(slotIndex):
				return
		if app.ENABLE_SELL_ITEM:
			if app.IsPressed(app.DIK_LCONTROL) and self.IsSellItems(slotIndex):
				self.questionDialog = uiCommon.QuestionDialog()
				self.questionDialog.SetText(localeInfo.SELL_ITEM_QUESTION)
				self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemSellQuestionDialog_OnAccept))
				self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemSellQuestionDialog_OnCancel))
				self.questionDialog.Open()
				self.questionDialog.slotIndex = slotIndex
				return
		if item.IsFlag(item.ITEM_FLAG_CONFIRM_WHEN_USE):
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM)
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
			self.questionDialog.Open()
			self.questionDialog.slotIndex = slotIndex

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

		elif player.GetItemTypeBySlot(slotIndex) == item.ITEM_TYPE_GACHA or player.GetItemTypeBySlot(slotIndex) == item.ITEM_TYPE_GIFTBOX:
			if app.ENABLE_SHOW_CHEST_DROP:
				if self.interface:
					if self.interface.dlgChestDrop:
						if not self.interface.dlgChestDrop.IsShow():
							self.interface.dlgChestDrop.Open(slotIndex)
							net.SendChestDropInfo(slotIndex)
							
		else:
			self.__SendUseItemPacket(slotIndex)
			
	def __UseItemSellQuestionDialog_OnCancel(self):
		self.OnCloseQuestionDialog()

	def __UseItemSellQuestionDialog_OnAccept(self):
		self.__SendSellItemPacket(self.questionDialog.slotIndex)
		self.OnCloseQuestionDialog()
		
	def __UseItemQuestionDialog_OnCancel(self):
		self.OnCloseQuestionDialog()

	def __UseItemQuestionDialog_OnAccept(self):
		self.__SendUseItemPacket(self.questionDialog.slotIndex)
		self.OnCloseQuestionDialog()

	def __SendUseItemToItemPacket(self, srcSlotPos, dstSlotPos):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemUseToItemPacket(srcSlotPos, dstSlotPos)

	def __SendUseItemPacket(self, slotPos):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemUsePacket(slotPos)

	def __SendMoveItemPacket(self, srcSlotPos, dstSlotPos, srcItemCount):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemMovePacket(srcSlotPos, dstSlotPos, srcItemCount)
		
	if app.ENABLE_SELL_ITEM:
		def IsSellItems(self, slotIndex):
			itemVnum = player.GetItemIndex(slotIndex)
			item.SelectItem(itemVnum)
			itemPrice = item.GetISellItemPrice()

			if itemPrice > 1:
				return True
				
			return False
			
		def __SendSellItemPacket(self, itemVNum):
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
				return
				
			net.SendItemSellPacket(itemVNum)

	def SetDragonSoulRefineWindow(self, wndDragonSoulRefine):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoulRefine = wndDragonSoulRefine

	if app.BL_TRANSMUTATION_SYSTEM:
		## HilightSlot Change
		def DeactivateSlot(self, slotindex, type):
			if type == wndMgr.HILIGHTSLOT_CHANGE_LOOK:
				self.__DelHighlightSlotChangeLook(slotindex)

		## HilightSlot Change
		def ActivateSlot(self, slotindex, type):
			if type == wndMgr.HILIGHTSLOT_CHANGE_LOOK:
				self.__AddHighlightSlotChangeLook(slotindex)
		
		def __AddHighlightSlotChangeLook(self, slotIndex):
			if not slotIndex in self.listHighlightedChangeLookSlot:
				self.listHighlightedChangeLookSlot.append(slotIndex)

		def __DelHighlightSlotChangeLook(self, slotIndex):
			if slotIndex in self.listHighlightedChangeLookSlot:
				if slotIndex >= player.INVENTORY_PAGE_SIZE:
					self.wndItem.DeactivateNewSlotEffect(slotIndex - (self.inventoryPageIndex * player.INVENTORY_PAGE_SIZE) )
				else:
					self.wndItem.DeactivateNewSlotEffect(slotIndex)
				self.listHighlightedChangeLookSlot.remove(slotIndex)

		def __HighlightSlot_Refresh(self):
			for i in xrange(self.wndItem.GetSlotCount()):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
				if slotNumber in self.listHighlightedChangeLookSlot:
					self.wndItem.ActivateNewSlotEffect(i)
					self.wndItem.SetNewSlotDiffuseColor(i, wndMgr.COLOR_TYPE_RED)

		def __HighlightSlot_Clear(self):
			for i in xrange(self.wndItem.GetSlotCount()):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
				if slotNumber in self.listHighlightedChangeLookSlot:
					self.wndItem.DeactivateNewSlotEffect(i)
					self.listHighlightedChangeLookSlot.remove(slotNumber)
					
	def OnMoveWindow(self, x, y):
		if self.wndBelt:
			self.wndBelt.AdjustPositionAndSize()

	def GetAcceAttribute(self, srcSlotPos):
		result = 0
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(srcSlotPos, i))
			
		if 0 != attrSlot:
			for c in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				type = attrSlot[c][0]
				if type != 0:
					result = result + 1
		
		return result
		
	def HighlightSlot(self, slot):
		if not slot in self.liHighlightedItems:
			self.liHighlightedItems.append(slot)
	
	def __RefreshHighlights(self):
		for i in xrange(player.INVENTORY_PAGE_SIZE):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
			if slotNumber in self.liHighlightedItems:
				self.wndItem.ActivateSlot(i)

	if app.ENABLE_AURA_SYSTEM:
		def __UseItemAuraQuestionDialog_OnAccept(self):
			self.questionDialog.Close()
			net.SendAuraRefineCheckIn(*(self.questionDialog.srcItem + self.questionDialog.dstItem + (player.GetAuraRefineWindowType(),)))
			self.questionDialog.srcItem = (0, 0)
			self.questionDialog.dstItem = (0, 0)

		def __UseItemAuraQuestionDialog_Close(self):
			self.questionDialog.Close()

			self.questionDialog.srcItem = (0, 0)
			self.questionDialog.dstItem = (0, 0)

		def __UseItemAura(self, slotIndex):
			AuraSlot = player.FineMoveAuraItemSlot()
			UsingAuraSlot = player.FindActivatedAuraSlot(player.INVENTORY, slotIndex)
			AuraVnum = player.GetItemIndex(slotIndex)
			item.SelectItem(AuraVnum)
			if player.GetAuraCurrentItemSlotCount() >= player.AURA_SLOT_MAX <= UsingAuraSlot:
				return

			if player.IsEquipmentSlot(slotIndex):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EQUIPITEM)
				return

			if player.GetAuraRefineWindowType() == player.AURA_WINDOW_TYPE_ABSORB:
				isAbsorbItem = False
				if item.GetItemType() == item.ITEM_TYPE_COSTUME:
					if item.GetItemSubType() == item.COSTUME_TYPE_AURA:
						if player.GetItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_DRAIN_ITEM_VNUM) == 0:
							if UsingAuraSlot == player.AURA_SLOT_MAX:
								if AuraSlot != player.AURA_SLOT_MAIN:
									return

								net.SendAuraRefineCheckIn(player.INVENTORY, slotIndex, player.AURA_REFINE, AuraSlot, player.GetAuraRefineWindowType())

						else:
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_ABSORBITEM)
							return

					else:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_ABSORBITEM)
						return

				elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
					if item.GetItemSubType() in [item.ARMOR_SHIELD, item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR]:
						if player.FindUsingAuraSlot(player.AURA_SLOT_MAIN) == player.NPOS():
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_REGISTER_AURAITEM)
							return

						isAbsorbItem = True
					else:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_ABSORBITEM)
						return

				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_ABSORBITEM)
					return

				if isAbsorbItem:
					if UsingAuraSlot == player.AURA_SLOT_MAX:
						if AuraSlot != player.AURA_SLOT_SUB:
							if player.FindUsingAuraSlot(player.AURA_SLOT_SUB) == player.NPOS():
								AuraSlot = player.AURA_SLOT_SUB
							else:
								return

						self.questionDialog = uiCommon.QuestionDialog()
						self.questionDialog.SetText(localeInfo.AURA_NOTICE_DEL_ABSORDITEM)
						self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemAuraQuestionDialog_OnAccept))
						self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemAuraQuestionDialog_Close))
						self.questionDialog.srcItem = (player.INVENTORY, slotIndex)
						self.questionDialog.dstItem = (player.AURA_REFINE, AuraSlot)
						self.questionDialog.Open()

			elif player.GetAuraRefineWindowType() == player.AURA_WINDOW_TYPE_GROWTH:
				if UsingAuraSlot == player.AURA_SLOT_MAX:
					if AuraSlot == player.AURA_SLOT_MAIN:
						if item.GetItemType() == item.ITEM_TYPE_COSTUME:
							if item.GetItemSubType() == item.COSTUME_TYPE_AURA:
								socketLevelValue = player.GetItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_CURRENT_LEVEL)
								curLevel = (socketLevelValue / 100000) - 1000
								curExp = socketLevelValue % 100000;
								if curLevel >= player.AURA_MAX_LEVEL:
									chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_MAX_LEVEL)
									return

								if curExp >= player.GetAuraRefineInfo(curLevel, player.AURA_REFINE_INFO_NEED_EXP):
									chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_GROWTHITEM)
									return

								net.SendAuraRefineCheckIn(player.INVENTORY, slotIndex, player.AURA_REFINE, AuraSlot, player.GetAuraRefineWindowType())

							else:
								chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)
								return

						else:
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)
							return

					elif AuraSlot == player.AURA_SLOT_SUB:
						if player.FindUsingAuraSlot(player.AURA_SLOT_MAIN) != player.NPOS():
							if item.GetItemType() == item.ITEM_TYPE_RESOURCE:
								if item.GetItemSubType() == item.RESOURCE_AURA:
									if UsingAuraSlot == player.AURA_SLOT_MAX:
										if AuraSlot != player.AURA_SLOT_SUB:
											return

										net.SendAuraRefineCheckIn(player.INVENTORY, slotIndex, player.AURA_REFINE, AuraSlot, player.GetAuraRefineWindowType())
								else:
									chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURARESOURCE)
									return

							else:
								chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURARESOURCE)
								return

						else:
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_REGISTER_AURAITEM)
							return

			elif player.GetAuraRefineWindowType() == player.AURA_WINDOW_TYPE_EVOLVE:
				if UsingAuraSlot == player.AURA_SLOT_MAX:
					if AuraSlot == player.AURA_SLOT_MAIN:
						if item.GetItemType() == item.ITEM_TYPE_COSTUME:
							if item.GetItemSubType() == item.COSTUME_TYPE_AURA:
								socketLevelValue = player.GetItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_CURRENT_LEVEL)
								curLevel = (socketLevelValue / 100000) - 1000
								curExp = socketLevelValue % 100000;
								if curLevel >= player.AURA_MAX_LEVEL:
									chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_MAX_LEVEL)
									return

								if curLevel != player.GetAuraRefineInfo(curLevel, player.AURA_REFINE_INFO_LEVEL_MAX) or curExp < player.GetAuraRefineInfo(curLevel, player.AURA_REFINE_INFO_NEED_EXP):
									chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EVOLUTION_ITEM)
									return

								if player.FindUsingAuraSlot(AuraSlot) != player.NPOS():
									return

								net.SendAuraRefineCheckIn(player.INVENTORY, slotIndex, player.AURA_REFINE, AuraSlot, player.GetAuraRefineWindowType())

							else:
								chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)
								return

						else:
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)
							return

					elif AuraSlot == player.AURA_SLOT_SUB:
						Cell = player.FindUsingAuraSlot(player.AURA_SLOT_MAIN)
						if Cell == player.NPOS():
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_REGISTER_AURAITEM)
							return

						socketLevelValue = player.GetItemMetinSocket(*(Cell + (player.ITEM_SOCKET_AURA_CURRENT_LEVEL,)))
						curLevel = (socketLevelValue / 100000) - 1000
						curExp = socketLevelValue % 100000;
						if curLevel >= player.AURA_MAX_LEVEL:
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_MAX_LEVEL)
							return

						if curExp < player.GetAuraRefineInfo(curLevel, player.AURA_REFINE_INFO_NEED_EXP):
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EVOLUTION_ITEM)
							return

						if AuraVnum != player.GetAuraRefineInfo(curLevel, player.AURA_REFINE_INFO_MATERIAL_VNUM):
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EVOLUTION_ITEM)
							return

						if player.GetItemCount(slotIndex) < player.GetAuraRefineInfo(curLevel, player.AURA_REFINE_INFO_MATERIAL_COUNT):
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EVOLUTION_ITEMCOUNT)
							return

						if UsingAuraSlot == player.AURA_SLOT_MAX:
							if AuraSlot != player.AURA_SLOT_MAX:
								if player.FindUsingAuraSlot(AuraSlot) != player.NPOS():
									return

							net.SendAuraRefineCheckIn(player.INVENTORY, slotIndex, player.AURA_REFINE, AuraSlot, player.GetAuraRefineWindowType())
