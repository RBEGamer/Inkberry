from DisplayFramework import ImplementedDevices, DeviceSpecification


class DeviceLookUpTable(object):
    # TODO REWORK TO FILE BASED TEMPLATES
    @staticmethod
    def get_hardware_definition(_hardware_type: ImplementedDevices,  spec: DeviceSpecification.DeviceSpecification = None) -> DeviceSpecification.DeviceSpecification:

        if spec is None:
            spec = DeviceSpecification.DeviceSpecification()


        if _hardware_type == ImplementedDevices.ImplementedDevices.SIMULATED:
            spec.screen_size_w = 640
            spec.screen_size_h = 480
            spec.content_scale = 1.0
            spec.display_orientation = DeviceSpecification.DisplayOrientation.DP_HORIZONTAL
            spec.image_filter = DeviceSpecification.DisplayImageFilters.DIF_NONE
            spec.colorspace = DeviceSpecification.DisplaySupportedColors.DSC_COLOR

        elif _hardware_type == ImplementedDevices.ImplementedDevices.MINIMAL or _hardware_type == ImplementedDevices.ImplementedDevices.INVALID:
            spec.screen_size_w = 640
            spec.screen_size_h = 480
            spec.content_scale = 1.0
            spec.display_orientation = DeviceSpecification.DisplayOrientation.DP_HORIZONTAL
            spec.image_filter = DeviceSpecification.DisplayImageFilters.DIF_NONE
            spec.colorspace = DeviceSpecification.DisplaySupportedColors.DSC_BW
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

        elif _hardware_type == ImplementedDevices.ImplementedDevices.INKBERRY_73_7COLOR:
            spec.screen_size_w = 800
            spec.screen_size_h = 480
            spec.content_scale = 1.0
            spec.display_orientation = DeviceSpecification.DisplayOrientation.DP_HORIZONTAL
            spec.image_filter = DeviceSpecification.DisplayImageFilters.DIF_NONE
            spec.colorspace = DeviceSpecification.DisplaySupportedColors.DSC_7COLOR



        return spec

    @staticmethod
    def get_compatible_hardware_models(_hardware_type: ImplementedDevices) -> [ImplementedDevices.ImplementedDevices]:
        rt: [ImplementedDevices.ImplementedDevices] = [_hardware_type]
        spec_orig = DeviceLookUpTable.get_hardware_definition(_hardware_type)
        # TODO REWORK
        for type in ImplementedDevices.ImplementedDevices:
            spec = DeviceLookUpTable.get_hardware_definition(type)

            if spec_orig.display_orientation == spec.display_orientation and spec_orig.screen_size_w == spec.screen_size_w and spec_orig.screen_size_h == spec.screen_size_h:
                rt.append(type)


        return rt



    @staticmethod
    def get_screen_size_w(_hardware_type: ImplementedDevices) -> int:
        return DeviceLookUpTable.get_hardware_definition(_hardware_type).screen_size_w

    @staticmethod
    def get_screen_size_h(_hardware_type: ImplementedDevices) -> int:
        return DeviceLookUpTable.get_hardware_definition(_hardware_type).screen_size_h

