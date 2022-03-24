import pyrealsense2 as rs
import numpy as np

class DepthCamera:
    def __init__(self):
        # reset camer before starting pipeline
        print("reset start")
        ctx = rs.context()
        devices = ctx.query_devices()
        for dev in devices:
            dev.hardware_reset()
        print("reset done")

        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        # Start streaming
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.pipeline.start(config)

    def get_frame(self):
        #depth frame (for depth map), color frame (for raw camera feed)
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        #add filters:
        #https://github.com/IntelRealSense/librealsense/blob/jupyter/notebooks/depth_filters.ipynb
        colorizer = rs.colorizer()
        decimation = rs.decimation_filter()
        spatial = rs.spatial_filter()
        temporal = rs.temporal_filter()
        hole_filling = rs.hole_filling_filter()


        frame = decimation.process(depth_frame)

        #depth_to_disparity = rs.disparity_transform(True)
        #frame = depth_to_disparity.process(frame)

        #frame = spatial.process(frame)
        #frame = temporal.process(frame)

        #disparity_to_depth = rs.disparity_transform(False)
        #frame = disparity_to_depth.process(frame)

        frame = hole_filling.process(frame)
        depth_image2 = np.asanyarray(colorizer.colorize(frame).get_data())


        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        if not depth_frame or not color_frame:
            return False, None, None
        return True, depth_image, color_image, depth_image2

    def release(self):
        self.pipeline.stop()