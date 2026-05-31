# tracertools
The tracertools package is a collection of Python functions deigned to streamline common tasks for connectomics researchers, particularly those related to the proofreading process. 

## Installation
Quick installation with pip isn't supported yet (but is planned for the future), so you'll have to intall the tracertools package manually from this GitHub repository by doing the following:

1. Open a terminal and navigate to the directory where you want the tracertools package to be stored.
2. Run the code `git clone https://github.com/jaybgager/tracertools.git` to make a local copy of the package at the location you naviagated to in step one. This will be create a folder named tracertools in that directory that's linked to the GitHub repository.
3. In the terminal, navigate one folder down, so that you're in the top-level (root) folder of the tracertools package by running the command `cd tracertools`.
4. In the terminal, run the command `pip install -e .`. This will tell Python's default installer, pip, to add the folder you're currently in to its list of importable packages. The `-e` modifier causes this installation to be "editable", meaning that if you make changes to the code stored in the tracertools folder, they'll take effect when you import tracertools into a python script. This is important for keeping the package up-to-date, so you don't have to reinatll it every time there are changes and lets you expriment with modifying the tools to meet your own needs. The `.` at the end just tells pip to install everything at the current directory location.

Now whenever you need to use a tracertools function, you can simply import it like any other package using the "import tracertools" code in any python script. Then, when you want to use a function, you add tracertools. in front of it. For example, if you wanted to use the get_current_seg_ids() function, you would use the following code:

```
import tracertools
fresh_ids = tracertools.get_current_seg_ids(
    datastack="brain_and_nerve_cord",
    seg_ids=[720575941586154052,720575941429544111]
)
```

You can also use and alias when importing the package; "tt" is a common choice. In that case, the above code would be modified slightly to look like this:

```
import tracertools as tt
fresh_ids = tt.get_current_seg_ids(
    datastack="brain_and_nerve_cord",
    seg_ids=[720575941586154052,720575941429544111]
)
```
## Glossary of Common Terms
Some terms used in the function descriptions are either uncommon or are used here to mean something very specific in the context of this package. These are defined below:


**bucket** - a server where files can be stored and accessed remotely. Often used for publicly hosting neuroglancer volumes containing meshes, annotation layers, or electron microscope (EM) image layers. Can also be used to host data tables for things like cell type labels, proofreading status, or synapse data. The functions that begin with the prefix `bucket_` relate to reading from and writing to buckets using the [cloudfiles](https://github.com/seung-lab/cloud-files) Python package.

**CAVE** - connectome annotation versioning engine, the software used to manage and interact with backend information about datastacks . This is done with the [caveclient](https://github.com/CAVEconnectome/CAVEclient) Python package, thorough documentation for which can be found [here](https://caveclient.readthedocs.io/en/latest/).

**chunkedgraph/pychunkedgraph/pcg** - the chunkedgraphis an organizational structure that holds the information about which supervoxels belong to which segments. It's created and managed by the [pychunkedgraph (pcg) python package](https://github.com/CAVEconnectome/PyChunkedGraph). Individual supervoxels are always considered to belong to the lowest layer, making them the "level 1 nodes", or "L1 nodes" for short. All the supervoxels belonging to a segment within a given cube of space, referred to as a "chunk", will be grouped together into a level 2 (L2) node. Multiple L2 nodes are grouped into an L3 node and so on until you reach a layer that contains all the supervoxels in the whole segment. For a more detailed explanation, read [this description](https://caveclient.readthedocs.io/en/latest/guide/chunkedgraph.html). Working with different layers can have advantages. For example, the L1 layer (usually just referred to as "the supervoxels") can provide detailed information at the cost of computational power, while the L2 nodes can provide information faster for less processing power, like cached 3D volume measurements - at the cost of being less reliable in certain contexts.

**cloudvolume** - a Python package that allows reading and writing of neuroglancer volumes directly in RAM without having to write to a hard drive, documentation for which can be found [here](https://github.com/seung-lab/cloud-volume). Used in a number of processes including mesh-related operations, creating and hosting volumes both locally or on a bucket, and spatial segment lookup.

**dataset** - the original image data (usually in the form of raw electron microscope images) for a specific brain (or other piece of tissue). Often identified by a descriptive acronym - e.g. Brain and Nerve Cord (BANC), Female Adult Fly Brain (FAFB) - or by the name of the organism that the tissue came from - e.g. "Minnie", "Basil".

**datastack** - all the data associated with a particular project associated with a given dataset. This can include aligned EM images, 3D segmentation data, and tables of information for things like synapses, cell type labels, or nucleus locations. It may alos include neuron skeletons, neuropil mesh layers, and other stack-specific information.

**edge (graph)** - a general term for the connection between two nodes in a graph. This could be a synapse between neurons, a connection between supervoxels in the same segment, or a link between two vertices of a mesh. Often stored as two numbers that in some way reference the ID or position of their endpoints in a list. 

**edge (mesh)** - the lines connecting a mesh's vertices, representing the places where the mesh surface changes direction. Stored as pairs of index numbers pointing to the position of their endpoints in the mesh's list of vertices (e.g. [vertex A index #, vertex B index #])

**face** - the flat planes that make up the surface of a 3D mesh. Can be any shape, but generally stored as triangles (sometimes called "tris") for rendering and mathematical analysis purposes. Can be stored either as lists/arrays of 3 points or 3 edges, depending on useage. May also be associated with a normal.

**graphene** - a data format backed by pychunkedgraph, used by cloudvolume and the Seung Lab's custom version of neuroglancer, documentation for which can be found [here](https://github.com/seung-lab/cloud-volume/wiki/Graphene).

**mesh** - a 3-dimensional shape, often representing a neuron, but sometimes used to depict other structures like organelles, nuclei, neuropils, or simply regions of space. Stored in literal terms as a collection of vertices, edges, and faces. A mesh is considered "watertight" if all its triangular faces are connected to exactly 3 other triangular faces (i.e. there are no "holes"). Many formats for storing mesh information exist, but this package primarily uses either those found in neuroglancer volumes or sometimes OBJ files. 

**neuroglancer (NG)** - a user interface (UI) for interacting with the 3D segmentation and rendering of neurons and other biological structures, the documentation for which can be found [here](https://github.com/google/neuroglancer). There are multiple branches of NG for specific purposes, like [FlyWire](https://github.com/seung-lab/ng-extend/tree/flywire) or [Spelunker](https://github.com/seung-lab/neuroglancer/tree/spelunker). Most of the functions in this package are built for use with Spelunker, the Seung Lab's current customized version of NG.

**normal (mesh)** - a ray (line with a direction) aimed perpendicular (sometimes reffered to as "orthogonal") to a flat plane. Often used to indicate what direction a mesh face is oriented for the purposes of rendering lighting.

**precomputed** - a common type of formatting for neuroglancer data layers that relies on doing complex mathematical operations ahead of time (pre-computing) to allow faster use by the end user.

**resolution** - the actual, physical dimensions in nanometers represented by one "unit" in the x, y, and z directions, stored as a list/array of 3 numbers (e.g. [4, 4, 45] for the voxel dimensions in the "brain and nerve_cord" datastack). Common derived terms include "viewer resolution" (the default voxel resolution used when viewing a datastack in neuroglancer), "mip0 resolution" (the voxel resolution of the raw electron microscope images for a dataset), and "nanometer resolution" (where the x-, y-, and z-resolutions are all 1 nanometer, often used for backend spatial information storage and mathematical calculations).

**root ID** - an umbrella term that can refer to the numeric identifier attached to a single supervoxel, chunkedgraph node, or segment. Appropriate to use when the entity in question can't be known ahead of time, as in the get_roots_from_points() function, which can return either a segment or supervoxel ID dependingon the user's input. Often used in other sources interchangeably with the term "segment ID", but won't be here.

**segmement/segmentation** - the current group of supervoxels that make up one or more neurons and their overall representation in 3D. Associated with a unique 18-digit numeric identifier (segment ID / seg ID) for a given version of a single segment. The term "segment ID" is often used interchangeably with the term "root ID" in other sources, but won't be here.

**supervoxel** - the smallest rearrangeable unit of a 3D segment, made up of multiple voxels. Not a consistent size. Sometimes referred to as the "watershed" layer because of [the type of algorithm](https://en.wikipedia.org/wiki/Watershed_(image_processing)) that led to their creation. Supervoxels cannot be broken apart, a quality sometimes referred to as being "atomic" (i.e. the smallest unbreakable constituent part of something). When referenceing the "nodes"/"leaves"/"layers" of the chunkedgraph, supervoxels are L1 - the foundational level. At any given time, a supervoxel will "belong to" a specific segment (and will therefore be associated with that segment's ID), but this assignment will change if that segment is edited.

**vertex** - a single point in 3D space connected to other points. Used to represent the boundaries of a 3D mesh. Stored as a list or array of 3 numbers (e.g. `[1,2,3]`) corresponding to the point's x, y, and z coordinates, either in nanometers, or in voxels - the measurements for which may change depending on the voxel resolution of the datastack you're working with. Plural vertices.

**volume** - a collection of neuroglancer-related assets that can include 2D image layers, 3D segmentation and meshing, segment skeletons, and annotations. Stored in a single folder/directory often named "image". Several formats exist depending on the type of mesh being used, more documentation about which can be found [here](https://github.com/google/neuroglancer/blob/master/src/datasource/precomputed/meshes.md). 

**voxel** - one unit of 3D space, shaped like a rectangular prism, the actual spatial dimensions of which vary from datastack to datastack. Compare to a 2-dimensional pixel.

## Functions
WORK IN PROGRESS
Below are basic descriptions of each function in the tracertools package, with instructions on their use. Examples will be added at a alter date.

# bucket_convert_colons
Converts any colons `:` in a string to triple-underscores `___`. Used to allow creation and downloading of neuroglancer legacy-format volumes (which by necessity must include colons in several file names) on Windows machines (which strictly prohibit the use of colons in file names).

# bucket_delete_file
Takes a file path on a cloudfiles-managed bucket and deletes the file.

# bucket_delete_folder
Takes a folder path on a cloudfiles-managed bucket and deletes the folder, including everything contained within. Includes a confirmation window that pops up to prevent accidental deletion.

# bucket_download_file
Takes a file path on a cloudfiles-managed bucket with the `bucket_path` argument and downloads the file. Tries to find the default Downloads folder automatically, but a specific path can be optionally passed with the `download_path` argument.

## License
The tracertools package is licensed under the GNU General Public License v3.0. See the [LICENSE](https://github.com/jaybgager/tracertools/blob/main/LICENSE) file for more details.