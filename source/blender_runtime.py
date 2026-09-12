"""Choose an available Cycles device without depending on one workstation."""
import os
import platform


def configure_cycles(scene):
    import bpy

    requested = os.environ.get('BLENDER_DEVICE', 'AUTO').upper()
    allowed = {'AUTO', 'CPU', 'METAL', 'OPTIX', 'CUDA', 'HIP', 'ONEAPI'}
    if requested not in allowed:
        raise ValueError(f'BLENDER_DEVICE must be one of {sorted(allowed)}')
    scene.cycles.device = 'CPU'
    if requested == 'CPU':
        return 'CPU'
    preferences = bpy.context.preferences.addons['cycles'].preferences
    backends = (['METAL'] if platform.system() == 'Darwin'
                else ['OPTIX', 'CUDA', 'HIP', 'ONEAPI'])
    if requested != 'AUTO':
        backends = [requested]
    for backend in backends:
        try:
            preferences.compute_device_type = backend
            preferences.get_devices()
        except (TypeError, ValueError, RuntimeError):
            continue
        if any(device.type == backend for device in preferences.devices):
            for device in preferences.devices:
                device.use = device.type == backend
            scene.cycles.device = 'GPU'
            return backend
    if requested != 'AUTO':
        raise RuntimeError(f'No Cycles device available for {requested}')
    return 'CPU'
