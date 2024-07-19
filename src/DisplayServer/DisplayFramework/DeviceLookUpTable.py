from DisplayFramework import ImplementedDevices, DeviceSpecification


class DeviceLookUpTable(object):
    # TODO REWORK TO FILE BASED TEMPLATES
    @staticmethod
    def get_hardware_definition(_hardware_type: ImplementedDevices) -> DeviceSpecification.DeviceSpecification:
        spec: DeviceSpecification.DeviceSpecification = DeviceSpecification.DeviceSpecification()


        if _hardware_type == ImplementedDevices.ImplementedDevices.SIMULATED:
            spec.screen_size_w = 640
            spec.screen_size_h = 480
            spec.content_scale = 1.0
            spec.display_orientation = DeviceSpecification.DisplayOrientation.DP_HORIZONTAL
            spec.image_filter = DeviceSpecification.DisplayImageFilters.DIF_NONE
            spec.colorspace = DeviceSpecification.DisplaySupportedColors.DSC_COLOR

        elif _hardware_type == ImplementedDevices.ImplementedDevices.INKPLATE10:
            spec.screen_size_w = 1200
            spec.screen_size_h = 820
            spec.content_scale = 1.0
            spec.display_orientation = DeviceSpecification.DisplayOrientation.DP_HORIZONTAL
            spec.image_filter = DeviceSpecification.DisplayImageFilters.DIF_NONE
            spec.colorspace = DeviceSpecification.DisplaySupportedColors.DSC_GRAY

        elif _hardware_type == ImplementedDevices.ImplementedDevices.INKBERRY_75_LAMINATED_BW:
            spec.screen_size_w = 800
            spec.screen_size_h = 480
            spec.content_scale = 1.0
            spec.display_orientation = DeviceSpecification.DisplayOrientation.DP_HORIZONTAL
            spec.image_filter = DeviceSpecification.DisplayImageFilters.DIF_DITHER
            spec.colorspace = DeviceSpecification.DisplaySupportedColors.DSC_BWR

        elif _hardware_type == ImplementedDevices.ImplementedDevices.INKBERRY_75_RBW:
            spec.screen_size_w = 800
            spec.screen_size_h = 480
            spec.content_scale = 1.0
            spec.display_orientation = DeviceSpecification.DisplayOrientation.DP_HORIZONTAL
            spec.image_filter = DeviceSpecification.DisplayImageFilters.DIF_DITHER
            spec.colorspace = DeviceSpecification.DisplaySupportedColors.DSC_BWR



        return spec

    @staticmethod
    def get_screen_size_w(_hardware_type: ImplementedDevices) -> int:
        return DeviceLookUpTable.get_hardware_definition(_hardware_type).screen_size_w

    @staticmethod
    def get_screen_size_h(_hardware_type: ImplementedDevices) -> int:
        return DeviceLookUpTable.get_hardware_definition(_hardware_type).screen_size_h
