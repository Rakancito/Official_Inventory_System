//Add at the end and before the last }

#ifdef ENABLE_ADDITIONAL_EQUIPMENT_PAGE
	PyModule_AddIntConstant(poModule, "ENABLE_ADDITIONAL_EQUIPMENT_PAGE", 1);
#else
	PyModule_AddIntConstant(poModule, "ENABLE_ADDITIONAL_EQUIPMENT_PAGE", 0);
#endif