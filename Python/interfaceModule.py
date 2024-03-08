# Add

if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
	import uiNewInventory
else:
	import uiInventory

# Search

		self.wndCharacter = None
		self.wndInventory = None

# After add

		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			self.wndEquipmentInventory = None	

# Add after
		wndInventory.BindInterfaceClass(self)

#This code
		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			wndEquipmentInventory = uiNewInventory.EquipmentWindow()
			wndEquipmentInventory.BindInterfaceClass(self)

# Search in 	def __MakeWindows(self):

		self.wndCharacter = wndCharacter
		self.wndInventory = wndInventory

#Add after

		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			self.wndEquipmentInventory = wndEquipmentInventory

# Search

		if self.wndInventory:
			self.wndInventory.Destroy()

#Add after

		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			if self.wndEquipmentInventory:
				self.wndEquipmentInventory.Destroy()

#Search

		del self.wndCharacter
		del self.wndInventory

#Add after

		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			del self.wndEquipmentInventory

#Search

	def RefreshInventory(self):
		self.wndTaskBar.RefreshQuickSlot()
		self.wndInventory.RefreshItemSlot()

#Add after

		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			self.wndEquipmentInventory.RefreshEquipSlotWindow()

#Search

		self.wndCharacter.Show()
		self.wndInventory.Show()

#Add after

		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			self.wndEquipmentInventory.Show()

#Search

		if self.wndInventory:
			self.wndInventory.Hide()

#Add after

		if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
			if self.wndEquipmentInventory:
				self.wndEquipmentInventory.Hide()

#Search 	def ToggleInventoryWindow(self): and replace all with this

	def ToggleInventoryWindow(self):
		if False == player.IsObserverMode():
			if False == self.wndInventory.IsShow():
				self.wndInventory.Show()
				self.wndInventory.SetTop()
				if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
					if False == self.wndEquipmentInventory.IsShow():
						self.wndEquipmentInventory.Show()
						self.wndEquipmentInventory.SetTop()
			else:
				self.wndInventory.OverOutItem()
				self.wndInventory.Close()
				if app.ENABLE_ADDITIONAL_EQUIPMENT_PAGE:
					if self.wndEquipmentInventory.IsShow():
						self.wndEquipmentInventory.OverOutItem()
						self.wndEquipmentInventory.Close()

#Search

self.wndInventory,\

#Add after

self.wndEquipmentInventory,\

