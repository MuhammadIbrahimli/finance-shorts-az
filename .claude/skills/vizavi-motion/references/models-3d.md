# Ready-Made 3D Models and Scene Integration

For a personal task, you may find and download suitable ready-made free models within the current request. Prefer GLB/glTF when compatible with the selected renderer and export. Check the exact asset and its terms; “free” does not mean unrestricted rights. Do not impose a blanket download ban because of hypothetical future commercialization or source-code distribution, and do not prohibit the user from showing devices in a video.

Use an actually available source and an ordinary permitted download. Do not bypass access restrictions or claim an inaccessible asset was obtained. Do not turn asset selection into unauthorized registration or integration setup. Choose from the [3D sources registry](3d-sources.md); do not invent unknown services, terms, or prices.

## Before using a model in a scene

1. Check the exact model/variant, format, and contents: mesh, UVs, textures, materials, rig/animations, and external dependencies. Open or render the actual file, not just the website preview.
2. Normalize units and scale, axes, position, orientation, origin/pivot. Check normals, edges, thickness, topology, transparency, roughness/metalness, texture color space, and renderer compatibility. Do not attribute WebGPU/TSL properties to an ordinary WebGL material.
3. Check texture availability after download, dimensions, paths, and alpha. Make sure the model holds together at the chosen shot size. Reduce heavy meshes/textures while preserving silhouette and necessary detail; check actual render speed and export path.
4. Set lighting, environment, exposure, camera, shadows, and contact for the chosen material. Plastic, metal, and glass should behave differently. A bright highlight or general gradient does not fix incorrect shape.
5. For a laptop, check the lid/base as separate parts and the hinge axis. Opening is the lid's relative rotation around the hinge, not rotation of the whole body. Check closed/open states, screen, original orientation, and ensure an unintended underside is not shown.

Conceal/reveal, labels, and camera should belong to one coherent spatial scene. In a close pass, preserve the main subject's focus and correct scale; do not cross the near plane. When replacing a model, recheck orientation, pivot, lighting, contact, and animation.

## Brief asset notes in the final result

List the actual websites/pages and specific files used: author/title, link, format, stated license or terms with the date checked, required attribution, and modifications. Rights may differ for code, model, textures, font, and music. If the intended use is genuinely restricted, state that accurately and choose a permitted alternative; do not turn ordinary personal downloads into a legal barrier. Do not confuse permission to view/download with permission to resell or distribute an asset.