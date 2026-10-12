def get_config(datastack):
    """
    Gets the in-house tracer-format config dictionary for a given datastack. 
    
    Useful for building neuroglancer states and querying backend cave tables.

    Argument
        datastack (str):
        the name of the CAVE datastack you want the config for
        for a list of currently-supported datastack names use get_supported_configs()

    Returns
        config (dict):
            the config dictionary for the requested datastack
    """

    # defines dictionary of config dicts for the supported datastacks
    configs = {
        # last updated 2026/10/9
        "basil-seg-aug" : {
            "alignment_cave_id": 4,
            "alignment_display_name": "Basil",
            "alignment_description" : "This is the first alignment of the 1mm x 1mm x 40um dataset IARPA dataset from mouse V1.",
            "alignment_name": "basil_v0",
            "cell_info_table_format" : None,
            "cell_info_table_name" : None,
            "dataset_name": "Basil",
            "datastack_description": "This is the largest segmentation volume of the basil dataset that covers layer 2/3 to layer 6.",
            "image_source" : "precomputed://middleauth+https://storage.googleapis.com/neuroglancer/basil_v0/son_of_alignment/v3.04_cracks_only_normalized_rechunked",
            "local_server" : "https://minnie.microns-daf.com",
            "neuropil_mesh_source" : None,
            "proofreading_table_format" : None,
            "proofreading_table_name" : None,
            "seg_source" : "precomputed://middleauth+https://storage.googleapis.com/neuroglancer/basil_v0/basil_full/seg-aug",
            "shortlink_server" : None,
            "skeleton_source" : None,
            "soma_table_format" : None,
            "soma_table_name" : None,
            "swamp_mesh_source" : None,
            "swamp_seg_ids": None,
            "synapse_table_format": None,
            "synapse_table_name": None,
            "tt_notes": "incomplete entry, gives network errors with for both seg and em",
            "viewer_2d_zoom" : 10,
            "viewer_3d_angle" : [0, 0, 0, 1],
            "viewer_3d_zoom" : 10000,
            "viewer_res" : [4, 4, 40],
            "viewer_site" : "https://spelunker.cave-explorer.org/", # officially None #
            "viewer_start_coords" : [],
            "volume_size" : [],
            "volume_min_coord" : [],
            "volume_max_coord" : [],
            "volume_center_coord": [],
            "whole_stack_mesh_source" : None,
            # --- unique entries below this line --- #
            "analysis_database": "ibs-forrestc-ux1.corp.alleninstitute.org",
        },
        # last updated 2026/10/09
        "brain_and_nerve_cord" : {
            "alignment_cave_id": 9,
            "alignment_display_name": "BANC",
            "alignment_description" : 'The BANC (said "the bank") is the Brain And Nerve Cord, a GridTape transmission electron microscopy dataset of a female adult Drosophila melanogaster\'s entire central nervous system. Visit https://banc.community for more information.',
            "alignment_name": "brain_and_nerve_cord",
            "cell_info_table_format" : "cell_std",
            "cell_info_table_name" : "cell_info",
            "dataset_name": "BANC",
            "datastack_description": None,
            "image_source" : "precomputed://gs://seunglab_lee_fly_cns_001_alignment/aligned/v0",
            "local_server" : "https://cave.fanc-fly.com",
            "neuropil_mesh_source" : None,
            "proofreading_table_format" : "proof_std",
            "proofreading_table_name" : "backbone_proofread",
            "seg_source" : "graphene://middleauth+https://cave.fanc-fly.com/segmentation/table/wclee_fly_cns_001",
            "shortlink_server" : None,
            "skeleton_source" : "precomputed://https://cave.fanc-fly.com/skeletoncache/api/v1/brain_and_nerve_cord/precomputed/skeleton",
            "soma_table_format" : None,
            "soma_table_name" : None,
            "swamp_mesh_source" : "https://c10s.pni.princeton.edu/tracers/swamps/banc/main|neuroglancer-precomputed:",
            "swamp_seg_ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            "synapse_table_format": "syn_std",
            "synapse_table_name": "synapses_v2",
            "tt_notes": None,
            "viewer_2d_zoom" : 4.12,
            "viewer_3d_angle" : [0, 1, 0, 0],
            "viewer_3d_zoom" : 360849,
            "viewer_res" : [4, 4, 45],
            "viewer_site" : "https://spelunker.cave-explorer.org/",
            "viewer_start_coords" : [125563, 118181, 2850],
            "volume_size" : [262144, 294912, 7010],
            "volume_min_coord" : [0, 0, 0],
            "volume_max_coord" : [262143, 294911, 7009],
            "volume_center_coord": [131027, 147460, 3505],
            "whole_stack_mesh_source" : "precomputed://gs://lee-lab_brain-and-nerve-cord-fly-connectome/region_outlines",
            # --- unique entries below this line --- #
            # hosting url for MANC datastack aligned comparison mesh
            "manc_seg_source": "precomputed://gs://lee-lab_brain-and-nerve-cord-fly-connectome/imported_meshes/manc_v1.2.1_meshes_elastix_tpsreg_240721",
        },
        # last updated 2026/10/09
        "brain_and_nerve_cord_public" : {
            "alignment_cave_id": 9,
            "alignment_display_name": "BANC",
            "alignment_description" : 'The BANC (said "the bank") is the Brain And Nerve Cord, a GridTape transmission electron microscopy dataset of a female adult Drosophila melanogaster\'s entire central nervous system. Visit https://banc.community for more information.',
            "alignment_name": "brain_and_nerve_cord",
            "cell_info_table_format" : "cell_std",
            "cell_info_table_name" : "cell_info",
            "dataset_name": "BANC",
            "datastack_description": "Public data release of BANC (Nature)",
            "image_source" : "precomputed://gs://seunglab_lee_fly_cns_001_alignment/aligned/v0",
            "local_server" : "https://cave.fanc-fly.com",
            "neuropil_mesh_source" : None,
            "proofreading_table_format" : "proof_std",
            "proofreading_table_name" : "backbone_proofread",
            "seg_source" : "graphene://https://cave.fanc-fly.com/segmentation/table/wclee_fly_cns_001_public",
            "shortlink_server" : None,
            "skeleton_source" : "precomputed://https://cave.fanc-fly.com/skeletoncache/api/v1/brain_and_nerve_cord_public/precomputed/skeleton",
            "soma_table_format" : None,
            "soma_table_name" : None,
            "swamp_mesh_source" : "https://c10s.pni.princeton.edu/tracers/swamps/banc/main|neuroglancer-precomputed:",
            "swamp_seg_ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            "synapse_table_format": "syn_std",
            "synapse_table_name": "synapses_v2",
            "tt_notes": None,
            "viewer_2d_zoom" : 4.12,
            "viewer_3d_angle" : [0, 1, 0, 0],
            "viewer_3d_zoom" : 360849,
            "viewer_res" : [4, 4, 45],
            "viewer_site" : "https://spelunker.cave-explorer.org/",
            "viewer_start_coords" : [125563, 118181, 2850],
            "volume_size" : [262144, 294912, 7010],
            "volume_min_coord" : [0, 0, 0],
            "volume_max_coord" : [262143, 294911, 7009],
            "volume_center_coord": [131027, 147460, 3505],
            "whole_stack_mesh_source" : "precomputed://gs://lee-lab_brain-and-nerve-cord-fly-connectome/region_outlines",
            # --- unique entries below this line --- #
            # hosting url for MANC datastack aligned comparison mesh
            "manc_seg_source": "precomputed://gs://lee-lab_brain-and-nerve-cord-fly-connectome/imported_meshes/manc_v1.2.1_meshes_elastix_tpsreg_240721",
        },
        # last updated 2026/10/9
        "fafb_v15_20221128025036" : {
            "alignment_cave_id": 8,
            "alignment_display_name": "FAFB_v15",
            "alignment_description" : "This is the 2022 alignment of the FAFB dataset from the seung lab",
            "alignment_name": "FAFB_v15",
            "cell_info_table_format" : None,
            "cell_info_table_name" : None,
            "dataset_name": "FAFB",
            "datastack_description": "fafb_v15 experiments for Ran",
            "image_source" : "precomputed://https://tigerdata.princeton.edu/sseung-test1/fafb-v15-alignment-temp/fine_final/z0_7063/v1/aligned/mip1",
            "local_server" : "https://minnie.microns-daf.com",
            "neuropil_mesh_source" : "precomputed://gs://flywire_neuropil_meshes/neuropils/neuropil_mesh_v141_v3",
            "proofreading_table_format" : None,
            "proofreading_table_name" : None,
            "seg_source" : "graphene://middleauth+https://minnie.microns-daf.com/segmentation/table/fafb_v15_20221128025036",
            "shortlink_server" : None,
            "skeleton_source" : None,
            "soma_table_format" : None,
            "soma_table_name" : None,
            "swamp_mesh_source" : None,
            "swamp_seg_ids": None,
            "synapse_table_format": None,
            "synapse_table_name": None,
            "tt_notes": "image source gives network error with and without middleauth",
            "viewer_2d_zoom" : 13.2,
            "viewer_3d_angle" : [0, 0, 0, -1],
            "viewer_3d_zoom" : 9600,
            "viewer_res" : [16, 16, 40],
            "viewer_site": "https://spelunker.cave-explorer.org/", # officially "https://neuromancer-seung-import.appspot.com/" #
            "viewer_start_coords" : [131071, 147456, 3505],
            "volume_size" : [270336, 147456, 7062],
            "volume_min_coord" : [0, 0, 0],
            "volume_max_coord" : [270335, 147455, 7061],
            "volume_center_coord": [135168, 73728, 3531],
            "whole_stack_mesh_source" : "precomputed://gs://flywire_neuropil_meshes/whole_neuropil/brain_mesh_v141.surf",
            # --- unique entries below this line --- #
        },
        # NEW last updated 2026/10/12
        "fanc_production_mar2021" : {
            "alignment_cave_id": 7,
            "alignment_display_name": "FANC",
            "alignment_description" : 'FANC (pronounced "fancy") is the Female Adult Nerve Cord, a GridTape-TEM dataset of an adult female Drosophila melanogaster\\\'s ventral nerve cord. Visit https://fanc.community for more information.',
            "alignment_name": "fanc_v4",
            "cell_info_table_format" : None,
            "cell_info_table_name" : None,
            "dataset_name": "FANC",
            "datastack_description": "This is the first version of the fanc dataset hosted in CAVE.",
            "image_source" : "precomputed://gs://lee-lab_female-adult-nerve-cord/alignmentV4/em/rechunked",
            "local_server" : "https://cave.fanc-fly.com",
            "neuropil_mesh_source" : None,
            "proofreading_table_format" : "proof_std", #!!!DOUBLE CHECK THIS!!!#
            "proofreading_table_name" : "proofread_first_pass",
            "seg_source" : "graphene://middleauth+https://cave.fanc-fly.com/segmentation/table/mar2021_prod",
            "shortlink_server" : None,
            "skeleton_source" : "precomputed://https://cave.fanc-fly.com/skeletoncache/api/v1/fanc_production_mar2021/precomputed/skeleton",
            "soma_table_format" : "soma_std", #!!!DOUBLE CHECK THIS!!!#
            "soma_table_name" : "neuron_somas_dec2022",
            "swamp_mesh_source" : None,
            "swamp_seg_ids": None,
            "synapse_table_format": "syn_std",
            "synapse_table_name": "synapses_nov2022",
            "tt_notes": None,
            "viewer_2d_zoom" : 10,
            "viewer_3d_angle" : [0, 0, 0, 1],
            "viewer_3d_zoom" : 10000,
            "viewer_res" : [4.3, 4.3, 45.0],
            "viewer_site" : "https://spelunker.cave-explorer.org/", # officially "https://neuroglancer-demo.appspot.com/"
            "viewer_start_coords" : [41984, 111616, 2205],
            "volume_size" : [83968, 223232, 4390],
            "volume_min_coord" : [0, 0, 10],
            "volume_max_coord" : [83968, 223232, 4400],
            "volume_center_coord": [41984, 111616, 2205],
            "whole_stack_mesh_source" : None,
            # --- unique entries below this line --- #
        },
        # last updated 2026/10/12
        "fanc_sandbox" : {
            "alignment_cave_id": 7,
            "alignment_display_name": "FANC",
            "alignment_description" : 'FANC (pronounced "fancy") is the Female Adult Nerve Cord, a GridTape-TEM dataset of an adult female Drosophila melanogaster\\\'s ventral nerve cord. Visit https://fanc.community for more information.',
            "alignment_name": "fanc_v4",
            "cell_info_table_format" : None,
            "cell_info_table_name" : None,
            "dataset_name": "FANC",
            "datastack_description": "This is the sandbox deployment of FANC",
            "image_source" : "precomputed://gs://lee-lab_female-adult-nerve-cord/alignmentV4/em/rechunked",
            "local_server" : "https://cave.fanc-fly.com",
            "neuropil_mesh_source" : None,
            "proofreading_table_format" : "proof_std",
            "proofreading_table_name" : None,
            "seg_source" : "graphene://https://cave.fanc-fly.com/segmentation/table/mar2021_test",
            "shortlink_server" : None,
            "skeleton_source" : None,
            "soma_table_format" : None,
            "soma_table_name" : None,
            "swamp_mesh_source" : None,
            "swamp_seg_ids": None,
            "synapse_table_format": None,
            "synapse_table_name": None,
            "tt_notes": None,
            "viewer_2d_zoom" : 3,
            "viewer_3d_angle" : [0, 0, -1, 1],
            "viewer_3d_zoom" : 200855,
            "viewer_res" : [],
            "viewer_site" : "https://spelunker.cave-explorer.org/",
            "viewer_start_coords" : [41984, 111616, 2205],
            "volume_size" : [83968, 223232, 4390],
            "volume_min_coord" : [0, 0, 10],
            "volume_max_coord" : [83968, 223232, 4400],
            "volume_center_coord": [41984, 111616, 2205],
            "whole_stack_mesh_source" : None,
            # --- unique entries below this line --- #
        },
        # last updated 2026/10/12
        "flywire_fafb_production" : {
            "alignment_cave_id": 2,
            "alignment_display_name": "FAFB_v14",
            "alignment_description" : "The seung lab's realignment of the FAFB dataset",
            "alignment_name": "fafb_seung_alignment_v0",
            "cell_info_table_format" : "cell_std", #CHECK THIS#
            "cell_info_table_name" : "neuron_information_v2",
            "dataset_name": "FAFB",
            "datastack_description": "The production segmentation for the flywire segmentation",
            "image_source" : "precomputed://gs://flywire_em/aligned/v1",
            "local_server" : "https://prod.flywire-daf.com",
            "neuropil_mesh_source" : "precomputed://gs://flywire_neuropil_meshes/neuropils/neuropil_mesh_v141_v3",
            "proofreading_table_format" : "proof_std", #CHECK#
            "proofreading_table_name" : "proofreading_status_public_v1",
            "seg_source" : "graphene://https://prodv1.flywire-daf.com/segmentation/1.0/fly_v31",
            "shortlink_server" : "https://globalv1.flywire-daf.com/nglstate/post",
            "skeleton_source" : "precomputed://https://prod.flywire-daf.com/skeletoncache/api/v1/flywire_fafb_production/precomputed/skeleton",
            "soma_table_format" : "soma_std", # CHECK THIS #
            "soma_table_name" : "nuclei_v1",
            "swamp_mesh_source" : None,
            "swamp_seg_ids": None,
            "synapse_table_format": "syn_flywire",
            "synapse_table_name": "synapses_nt_v1",
            "tt_notes": None,
            "viewer_2d_zoom" : 13.2,
            "viewer_3d_angle" : [0, 0, 0, -1],
            "viewer_3d_zoom" : 9600,
            "viewer_res" : [4, 4, 40],
            "viewer_site" : "https://ngl.flywire.ai/",
            "viewer_start_coords" : [131071, 147456, 3505],
            "volume_size" : [270336, 147456, 7062],
            "volume_min_coord" : [0, 0, 0],
            "volume_max_coord" : [270335, 147455, 7061],
            "volume_center_coord": [135168, 73728, 3531],
            "whole_stack_mesh_source" : "precomputed://gs://flywire_neuropil_meshes/whole_neuropil/brain_mesh_v141.surf",
            # --- unique entries below this line --- #
            # proofreading review table
            "proofreading_review_table_name": "proofreading_review_public_v1",
        },
        # last updated 2026/10/12
        "flywire_fafb_public" : {
            "alignment_cave_id": 2,
            "alignment_display_name": "FAFB_v14",           
            "alignment_description" : "The seung lab's realignment of the FAFB dataset",
            "alignment_name": "fafb_seung_alignment_v0",
            "cell_info_table_format" : None,
            "cell_info_table_name" : None,
            "dataset_name": "FAFB",
            "datastack_description": "The public segmentation for the flywire segmentation",
            "image_source" : "precomputed://gs://flywire_em/aligned/v1",
            "local_server" : "https://prod.flywire-daf.com",
            "neuropil_mesh_source" : "precomputed://gs://flywire_neuropil_meshes/neuropils/neuropil_mesh_v141_v3",
            "proofreading_table_format" : None,
            "proofreading_table_name" : None,
            "seg_source" : "graphene://https://prod.flywire-daf.com/segmentation/1.0/flywire_public",
            "shortlink_server" : "https://globalv1.flywire-daf.com/nglstate/post",
            "skeleton_source" : "precomputed://https://prod.flywire-daf.com/skeletoncache/api/v1/flywire_fafb_public/precomputed/skeleton",
            "soma_table_format" : "soma_std", # CHECK THIS #
            "soma_table_name" : "nuclei_v1",
            "swamp_mesh_source" : None,
            "swamp_seg_ids": None,
            "synapse_table_format": None,
            "synapse_table_name": None,
            "tt_notes": None,
            "viewer_2d_zoom" : 13.2,
            "viewer_3d_angle" : [0, 0, 0, -1],
            "viewer_3d_zoom" : 9600,
            "viewer_res" : [4, 4, 40],
            "viewer_site" : "https://ngl.flywire.ai/",
            "viewer_start_coords" : [131071, 147456, 3505],
            "volume_size" : [270336, 147456, 7062],
            "volume_min_coord" : [0, 0, 0],
            "volume_max_coord" : [270335, 147455, 7061],
            "volume_center_coord": [135168, 73728, 3531],
            "whole_stack_mesh_source" : "precomputed://gs://flywire_neuropil_meshes/whole_neuropil/brain_mesh_v141.surf",
            # --- unique entries below this line --- #
        },
        # last updated 2026/10/12
        "flywire_fafb_sandbox" : {
            "alignment_cave_id": 2,
            "alignment_display_name": "FAFB_v14",           
            "alignment_description" : "The seung lab's realignment of the FAFB dataset",
            "alignment_name": "fafb_seung_alignment_v0",
            "cell_info_table_format" : None,
            "cell_info_table_name" : None,
            "dataset_name": "FAFB",
            "datastack_description": "The sandbox segmentation of flywire",
            "image_source" : "precomputed://gs://flywire_em/aligned/v1",
            "local_server" : "https://prod.flywire-daf.com",
            "neuropil_mesh_source" : "precomputed://gs://flywire_neuropil_meshes/neuropils/neuropil_mesh_v141_v3",
            "proofreading_table_format" : None,
            "proofreading_table_name" : None,
            "seg_source" : "graphene://https://prodv1.flywire-daf.com/segmentation/1.0/fly_v26",
            "shortlink_server" : None,
            "skeleton_source" : "precomputed://https://prod.flywire-daf.com/skeletoncache/api/v1/flywire_fafb_public/precomputed/skeleton",
            "soma_table_format" : "soma_std",#CHECK#
            "soma_table_name" : "nuclei_v1",
            "swamp_mesh_source" : None,
            "swamp_seg_ids": None,
            "synapse_table_format": None,
            "synapse_table_name": None,
            "tt_notes": None,
            "viewer_2d_zoom" : 13.2,
            "viewer_3d_angle" : [0, 0, 0, -1],
            "viewer_3d_zoom" : 2440,
            "viewer_res" : [4, 4, 40],
            "viewer_site" : "https://ngl.flywire.ai/", # officially None #
            "viewer_start_coords" : [131071, 147456, 3505],
            "volume_size" : [270336, 147456, 7062],
            "volume_min_coord" : [0, 0, 0],
            "volume_max_coord" : [270335, 147455, 7061],
            "volume_center_coord": [135168, 73728, 3531],
            "whole_stack_mesh_source" : "precomputed://gs://flywire_neuropil_meshes/whole_neuropil/brain_mesh_v141.surf",
            # --- unique entries below this line --- #
        },
        # # last updated 2026/10/12
        # "male_adult_nerve_cord" : {
        #     "alignment_cave_id": None,
        #     "alignment_display_name": "",
        #     "alignment_description" : "",
        #     "alignment_name": "",
        #     "cell_info_table_format" : "cell_std",
        #     "cell_info_table_name" : "",
        #     "dataset_name": "MANC",
        #     "datastack_description": "",
        #     "image_source" : "precomputed://gs://flyem-vnc-2-26-213dba213ef26e094c16c860ae7f4be0/v3_emdata_clahe_xy/jpeg",
        #     "local_server" : "",
        #     "neuropil_mesh_source" : "precomputed://gs://flyem-vnc-roi-d5f392696f7a48e27f49fa1a9db5ee3b/roi-202208",
        #     "proofreading_table_format" : "proof_std",
        #     "proofreading_table_name" : "",
        #     "seg_source" : "precomputed://gs://manc-seg-v1p2/manc-seg-v1.2",
        #     "shortlink_server" : "",
        #     "skeleton_source" : "",
        #     "soma_table_format" : "soma_std",
        #     "soma_table_name" : "",
        #     "swamp_mesh_source" : "",
        #     "swamp_seg_ids": [],
        #     "synapse_table_format": "syn_std",
        #     "synapse_table_name": "",
        #     "tt_notes": "not CAVE-hosted; https://www.neurotrailblazers.org/datasets/catalog/manc/",
        #     "viewer_2d_zoom" : 10,
        #     "viewer_3d_angle" : [0,0,0,1],
        #     "viewer_3d_zoom" : 10000,
        #     "viewer_res" : [8, 8, 8],
        #     "viewer_site" : "https://spelunker.cave-explorer.org/", # officially None #
        #     "viewer_start_coords" : [],
        #     "volume_size" : [],
        #     "volume_min_coord" : [],
        #     "volume_max_coord" : [],
        #     "volume_center_coord": [],
        #     "whole_stack_mesh_source" : "precomputed://gs://flyem-vnc-roi-d5f392696f7a48e27f49fa1a9db5ee3b/all-vnc-roi",
        #     # --- unique entries below this line --- #
        #     # mesh of nerve bundles #
        #     "nerve_mesh_source_url": "precomputed://gs://flyem-vnc-roi-d5f392696f7a48e27f49fa1a9db5ee3b/nerve-roi-202301",
        #     # annotation layer for presynaptic points #
        #     "presyn_anno_layer_source_url": "precomputed://gs://manc-seg-v1p2/manc-v1.2-synapse-partners-minconf-0.0.precomputed",
        #     # annotation layer for postsynaptic points #
        #     "postsyn_anno_layer_source_url": "precomputed://gs://manc-seg-v1p2/manc-v1.2-synapse-partners-minconf-0.0.precomputed",
        # },
        # last updated 2026/10/12
        "minnie35_phase3_v0" : {
            "alignment_cave_id": 6,
            "alignment_display_name": "Minnie35",          
            "alignment_description" : "this is the first alignment of minnie35, the smaller portion of minnie, it is adjacent to minnie65_phase3",
            "alignment_name": "minnie35_v0",
            "cell_info_table_format" : None,
            "cell_info_table_name" : None,
            "dataset_name": "minnie35",
            "datastack_description": None,
            "image_source" : "precomputed://https://bossdb-open-data.s3.amazonaws.com/iarpa_microns/minnie/minnie35/em",
            "local_server" : "https://minnie.microns-daf.com",
            "neuropil_mesh_source" : None,
            "proofreading_table_format" : None,
            "proofreading_table_name" : None,
            "seg_source" : "graphene://https://minnie.microns-daf.com/segmentation/table/minnie35_p3_v1",
            "shortlink_server" : None,
            "skeleton_source" : None,
            "soma_table_format" : None,
            "soma_table_name" : None,
            "swamp_mesh_source" : None,
            "swamp_seg_ids": None,
            "synapse_table_format": None,
            "synapse_table_name": None,
            "tt_notes": "segmentation requires authorization to access",
            "viewer_2d_zoom" : 3,
            "viewer_3d_angle" : [0, 0, 0, 1],
            "viewer_3d_zoom" : 666863,
            "viewer_res" : [4, 4, 40],
            "viewer_site" : "https://spelunker.cave-explorer.org/", # officially None #
            "viewer_start_coords" : [240640, 207872, 11376],
            "volume_size" : [425984, 360448, 6944],
            "volume_min_coord" : [27648, 27648, 7904],
            "volume_max_coord" : [453632, 388096, 14848],
            "volume_center_coord": [240640, 207872, 11376],
            "whole_stack_mesh_source" : None,
            # --- unique entries below this line --- #
            # another name for the parent dataset
            "dataset_alias": "cortex35",
        },
        # last updated 2026/10/12
        "minnie35_public_v0" : {
            "alignment_cave_id": 6,
            "alignment_display_name": "Minnie35",            
            "alignment_description" : "this is the first alignment of minnie35, the smaller portion of minnie, it is adjacent to minnie65_phase3",
            "alignment_name": "minnie35_v0",
            "cell_info_table_format" : None,
            "cell_info_table_name" : None,
            "dataset_name": "minnie35",
            "datastack_description": None,
            "image_source" : "precomputed://https://bossdb-open-data.s3.amazonaws.com/iarpa_microns/minnie/minnie35/em",
            "local_server" : "https://minnie.microns-daf.com",
            "neuropil_mesh_source" : None,
            "proofreading_table_format" : None,
            "proofreading_table_name" : None,
            "seg_source" : "graphene://https://minnie.microns-daf.com/segmentation/table/minnie35_public_v0",
            "shortlink_server" : None,
            "skeleton_source" : None,
            "soma_table_format" : None,
            "soma_table_name" : None,
            "swamp_mesh_source" : None,
            "swamp_seg_ids": None,
            "synapse_table_format": None,
            "synapse_table_name": None,
            "tt_notes": "segmentation requires authorization to access", #CHECK MIDDLEAUTH#
            "viewer_2d_zoom" : 3,
            "viewer_3d_angle" : [0, 0, 0, 1],
            "viewer_3d_zoom" : 666863,
            "viewer_res" : [4, 4, 40],
            "viewer_site" : "https://spelunker.cave-explorer.org/", # officially None #
            "viewer_start_coords" : [240640, 207872, 11376],
            "volume_size" : [425984, 360448, 6944],
            "volume_min_coord" : [27648, 27648, 7904],
            "volume_max_coord" : [453632, 388096, 14848],
            "volume_center_coord": [240640, 207872, 11376],
            "whole_stack_mesh_source" : None,
            # --- unique entries below this line --- #
            # another name for the parent dataset
            "dataset_alias": "cortex35",
        },
        # last updated 2026/10/12
        "minnie65_phase2_flat" : {
            "alignment_cave_id": 5,
            "alignment_display_name": None,
            "alignment_description" : "This is the first alignment of the 1mm x 1mm x 40um dataset IARPA dataset from mouse V1.",
            "alignment_name": "minnie65_phase2",
            "cell_info_table_format" : None,
            "cell_info_table_name" : None,
            "dataset_name": "minnie65",
            "datastack_description": "This contains the flat segmentation of the phase2 alignment and segmentation of Minnie65.",
            "image_source" : "precomputed://https://s3-hpcrc.rc.princeton.edu/minnie65/aligned_image",
            "local_server" : "https://minnie.microns-daf.com",
            "neuropil_mesh_source" : None,
            "proofreading_table_format" : None,
            "proofreading_table_name" : None,
            "seg_source" : "precomputed://https://storage.googleapis.com/microns-seunglab/minnie65/seg_minnie65_0",
            "shortlink_server" : None,
            "skeleton_source" : "precomputed://middleauth+https://minnie.microns-daf.com/skeletoncache/api/v1/minnie65_phase3_v1/precomputed/skeleton",
            "soma_table_format" : None,
            "soma_table_name" : None,
            "swamp_mesh_source" : None,
            "swamp_seg_ids": None,
            "synapse_table_format": None,
            "synapse_table_name": None,
            "tt_notes": "image source seems to be defunct",
            "viewer_2d_zoom" : 3,
            "viewer_3d_angle" : [0, 0, 0, 1],
            "viewer_3d_zoom" : 1215104,
            "viewer_res" : [4, 4, 40],
            "viewer_site" : "https://neuromancer-seung-import.appspot.com/", # officially None #
            "viewer_start_coords" : [245194, 191667, 21354],
            "volume_size" : [384848, 262102, 13008],
            "volume_min_coord" : [52770, 60616, 14850],
            "volume_max_coord" : [437618, 322718, 27858],
            "volume_center_coord": [245194, 191667, 21354],
            "whole_stack_mesh_source" : None,
            # --- unique entries below this line --- #
            # another name for the parent dataset
            "dataset_alias": "cortex65"
        },
        # last updated 2026/10/12
        "minnie65_phase3_v0" : {
            "alignment_cave_id": 1,
            "alignment_display_name": "Minnie65",           
            "alignment_description" : "This is the second alignment of the IARPA 'minnie65' dataset, completed in the spring of 2020 that used the seamless approach.",
            "alignment_name": "minnie65_phase3",
            "cell_info_table_format" : None,
            "cell_info_table_name" : None,
            "dataset_name": "minnie65",
            "datastack_description": "This is the initial dynamic segmentation of minnie65 phase 3, for which no proofreading is available.",
            "image_source" : "precomputed://https://bossdb-open-data.s3.amazonaws.com/iarpa_microns/minnie/minnie65/em",
            "local_server" : "https://minnie.microns-daf.com",
            "neuropil_mesh_source" : None,
            "proofreading_table_format" : None,
            "proofreading_table_name" : None,
            "seg_source" : "graphene://https://minniev1.microns-daf.com/segmentation/table/minnie3_v0",
            "shortlink_server" : None,
            "skeleton_source" : "precomputed://middleauth+https://minnie.microns-daf.com/skeletoncache/api/v1/minnie65_phase3_v1/precomputed/skeleton",
            "soma_table_format" : None,
            "soma_table_name" : None,
            "swamp_mesh_source" : None,
            "swamp_seg_ids": None,
            "synapse_table_format": None,
            "synapse_table_name": None,
            "tt_notes": None,
            "viewer_2d_zoom" : 3,
            "viewer_3d_angle" : [0, 0, 0, 1],
            "viewer_3d_zoom" : 1215104,
            "viewer_res" : [4, 4, 40],
            "viewer_site" : "https://neuromancer-seung-import.appspot.com/",
            "viewer_start_coords" : [245194, 191667, 21354],
            "volume_size" : [384848, 262102, 13008],
            "volume_min_coord" : [52770, 60616, 14850],
            "volume_max_coord" : [437618, 322718, 27858],
            "volume_center_coord": [245194, 191667, 21354],
            "whole_stack_mesh_source" : None,
            # --- unique entries below this line --- #
            # another name for the parent dataset
            "dataset_alias": "cortex65",
        },
        # last updated 2026/10/12
        "minnie65_phase3_v1" : {
            "alignment_cave_id": 1,
            "alignment_display_name": "Minnie65",           
            "alignment_description" : "This is the second alignment of the IARPA 'minnie65' dataset, completed in the spring of 2020 that used the seamless approach.",
            "alignment_name": "minnie65_phase3",
            "cell_info_table_format" : None,
            "cell_info_table_name" : None,
            "dataset_name": "minnie65",
            "datastack_description": "This is the first version of Minnie that has proofreading enabled. Was first enabled on June 24, 2020.",
            "image_source" : "precomputed://https://bossdb-open-data.s3.amazonaws.com/iarpa_microns/minnie/minnie65/em",
            "local_server" : "https://minnie.microns-daf.com",
            "neuropil_mesh_source" : None,
            "proofreading_table_format" : None,
            "proofreading_table_name" : None,
            "seg_source" : "graphene://middleauth+https://minnie.microns-daf.com/segmentation/table/minnie3_v1",
            "shortlink_server" : None,
            "skeleton_source" : "precomputed://middleauth+https://minnie.microns-daf.com/skeletoncache/api/v1/minnie65_phase3_v1/precomputed/skeleton",
            "soma_table_format" : "soma_std",#CHECK#
            "soma_table_name" : "nucleus_neuron_svm",
            "swamp_mesh_source" : None,
            "swamp_seg_ids": None,
            "synapse_table_format": "syn_std",#CHECK#
            "synapse_table_name": "synapses_pni_2",
            "tt_notes": None,
            "viewer_2d_zoom" : 3,
            "viewer_3d_angle" : [0, 0, 0, 1],
            "viewer_3d_zoom" : 1215104,
            "viewer_res" : [4, 4, 40],
            "viewer_site" : "https://spelunker.cave-explorer.org/",
            "viewer_start_coords" : [245194, 191667, 21354],
            "volume_size" : [384848, 262102, 13008],
            "volume_min_coord" : [52770, 60616, 14850],
            "volume_max_coord" : [437618, 322718, 27858],
            "volume_center_coord": [245194, 191667, 21354],
            "whole_stack_mesh_source" : None,
            # --- unique entries below this line --- #
            # another name for the parent dataset
            "dataset_alias": "cortex65",
        },
        # last updated 2026/10/12
        "minnie65_public" : {
            "alignment_cave_id": 1,
            "alignment_display_name": "Minnie65",           
            "alignment_description" : "This is the second alignment of the IARPA 'minnie65' dataset, completed in the spring of 2020 that used the seamless approach.",
            "alignment_name": "minnie65_phase3",
            "cell_info_table_format" : None,
            "cell_info_table_name" : None,
            "dataset_name": "minnie65",
            "datastack_description": "This is the publicly released version of the minnie65 volume and segmentation.",
            "image_source" : "precomputed://https://bossdb-open-data.s3.amazonaws.com/iarpa_microns/minnie/minnie65/em",
            "local_server" : "https://minnie.microns-daf.com",
            "neuropil_mesh_source" : None,
            "proofreading_table_format" : None,
            "proofreading_table_name" : None,
            "seg_source" : "graphene://https://minnie.microns-daf.com/segmentation/table/minnie65_public",
            "shortlink_server" : None,
            "skeleton_source" : "precomputed://middleauth+https://minnie.microns-daf.com/skeletoncache/api/v1/minnie65_public/precomputed/skeleton/",
            "soma_table_format" : "soma_std",#CHECK#
            "soma_table_name" : "nucleus_detection_v0",
            "swamp_mesh_source" : None,
            "swamp_seg_ids": None,
            "synapse_table_format": "syn_std",#CHECK#
            "synapse_table_name": "synapses_pni_2",
            "tt_notes": None,
            "viewer_2d_zoom" : 3,
            "viewer_3d_angle" : [0, 0, 0, 1],
            "viewer_3d_zoom" : 1215104,
            "viewer_res" : [4, 4, 40],
            "viewer_site" : "https://spelunker.cave-explorer.org/",
            "viewer_start_coords" : [245194, 191667, 21354],
            "volume_size" : [384848, 262102, 13008],
            "volume_min_coord" : [52770, 60616, 14850],
            "volume_max_coord" : [437618, 322718, 27858],
            "volume_center_coord": [245194, 191667, 21354],
            "whole_stack_mesh_source" : None,
            # --- unique entries below this line --- #
            # another name for the parent dataset
            "dataset_alias": "cortex65",
        },
        # last updated 2026/10/12
        "minnie65_sandbox" : {
            "alignment_cave_id": 1,
            "alignment_display_name": "Minnie65",           
            "alignment_description" : "This is the second alignment of the IARPA 'minnie65' dataset, completed in the spring of 2020 that used the seamless approach.",
            "alignment_name": "minnie65_phase3",
            "cell_info_table_format" : None,
            "cell_info_table_name" : None,
            "dataset_name": "minnie65",
            "datastack_description": "Sandbox dataset for Minnie65 segmentation",
            "image_source" : "graphene://https://minnie.microns-daf.com/segmentation/table/minnie3_v1_sandbox",
            "local_server" : "https://minnie.microns-daf.com",
            "neuropil_mesh_source" : None,
            "proofreading_table_format" : None,
            "proofreading_table_name" : None,
            "seg_source" : "graphene://https://minniev1.microns-daf.com/segmentation/table/minnie3_v0",
            "shortlink_server" : None,
            "skeleton_source" : None,
            "soma_table_format" : None,
            "soma_table_name" : None,
            "swamp_mesh_source" : None,
            "swamp_seg_ids": None,
            "synapse_table_format": None,
            "synapse_table_name": None,
            "tt_notes": "segmentation requires authorization to access?",
            "viewer_2d_zoom" : 3,
            "viewer_3d_angle" : [0, 0, 0, 1],
            "viewer_3d_zoom" : 1215104,
            "viewer_res" : [4, 4, 40],
            "viewer_site" : "https://spelunker.cave-explorer.org/", # officially None #
            "viewer_start_coords" : [245194, 191667, 21354],
            "volume_size" : [384848, 262102, 13008],
            "volume_min_coord" : [52770, 60616, 14850],
            "volume_max_coord" : [437618, 322718, 27858],
            "volume_center_coord": [245194, 191667, 21354],
            "whole_stack_mesh_source" : None,
            # --- unique entries below this line --- #
            # another name for the parent dataset
            "dataset_alias": "cortex65",
        },
        # last updated 2026/10/12
        "mrgd" : {
            "alignment_cave_id": 10,
            "alignment_display_name": "MrgD",           
            "alignment_description" : "Mouse dorsal spine",
            "alignment_name": "mrgd",
            "cell_info_table_format" : None,
            "cell_info_table_name" : None,
            "dataset_name": "MrgD",
            "datastack_description": None,
            "image_source" : "precomputed://gs://zetta_lee_mouse_spinal_cord_001_image/dorsal_sections/dorsal_sections_500_jpeg",
            "local_server" : "https://cave.fanc-fly.com",
            "neuropil_mesh_source" : None,
            "proofreading_table_format" : None,
            "proofreading_table_name" : None,
            "seg_source" : "graphene://https://cave.fanc-fly.com/segmentation/table/mouse_dorsal_spine",
            "shortlink_server" : None,
            "skeleton_source" : None,
            "soma_table_format" : None,
            "soma_table_name" : None,
            "swamp_mesh_source" : None,
            "swamp_seg_ids": None,
            "synapse_table_format": None,
            "synapse_table_name": None,
            "tt_notes": None,
            "viewer_2d_zoom" : 8,
            "viewer_3d_angle" : [0, 0, 0, 1],
            "viewer_3d_zoom" : 14764,
            "viewer_res" : [4, 4, 45],
            "viewer_site" : "https://neuromancer-seung-import.appspot.com",
            "viewer_start_coords" : [100863, 41471, 249],
            "volume_size" : [201727, 82943, 498],
            "volume_min_coord" : [0, 0, 0],
            "volume_max_coord" : [201727, 82943, 498],
            "volume_center_coord": [100863, 41471, 249],
            "whole_stack_mesh_source" : None,
            # --- unique entries below this line --- #
        },
        # last updated 2026/10/12
        "pinky_sandbox" : {
            "alignment_cave_id": 3,
            "alignment_display_name": "Pinky",           
            "alignment_description" : "The MiCrONS phase 2 100um dataset from layer 2/3 of p32 mouse visual cortex.",
            "alignment_name": "pinky100",
            "cell_info_table_format" : None,
            "cell_info_table_name" : None,
            "dataset_name": "Pinky",
            "datastack_description": "This is a sandbox segmentation for pinky that runs on the same chunkedgraph version as minnie, but has had very little proofreading done, and is used for testing purposes and not science.",
            "image_source" : "precomputed://https://bossdb-open-data.s3.amazonaws.com/iarpa_microns/pinky/em",
            "local_server" : "https://minnie.microns-daf.com",
            "neuropil_mesh_source" : None,
            "proofreading_table_format" : None,
            "proofreading_table_name" : None,
            "seg_source" : "graphene://middleauth+https://minnie.microns-daf.com/segmentation/table/pinky_nf_v2",
            "shortlink_server" : None,
            "skeleton_source" : None,
            "soma_table_format" : "soma_std",#CHECK#
            "soma_table_name" : "nuclei",
            "swamp_mesh_source" : None,
            "swamp_seg_ids": None,
            "synapse_table_format": "syn_std", #CHECK#
            "synapse_table_name": "synapses",
            "tt_notes": None,
            "viewer_2d_zoom" : 3,
            "viewer_3d_angle" : [0, 0, 0, 1],
            "viewer_3d_zoom" : 60496,
            "viewer_res" : [4, 4, 40],
            "viewer_site" : "https://spelunker.cave-explorer.org", # officially "https://neuromancer-seung-import.appspot.com/" #
            "viewer_start_coords" : [79155, 56093, 1089],
            "volume_size" : [85926, 51070, 2136],
            "volume_min_coord" : [36192, 30558, 21],
            "volume_max_coord" : [122118, 81628, 2157],
            "volume_center_coord": [79155, 56093, 1089],
            "whole_stack_mesh_source" : None,
            # --- unique entries below this line --- #
            # another name for the dataset
            "dataset_alias": "layer 2/3",
        },
        # last updated 2026/10/
        "stroeh_mouse_retina" : {
            "alignment_cave_id": 14,
            "alignment_display_name": None,           
            "alignment_description" : None,
            "alignment_name": "stroeh_mouse_retina",
            "cell_info_table_format" : None,
            "cell_info_table_name" : None,
            "dataset_name": "stroeh_mouse_retina",
            "datastack_description": None,
            "image_source" : "precomputed://gs://stroeh_sem_mouse_retina/image/v2",
            "local_server" : "https://minnie.microns-daf.com",
            "neuropil_mesh_source" : None,
            "proofreading_table_format" : None,
            "proofreading_table_name" : None,
            "seg_source" : "graphene://middleauth+https://minnie.microns-daf.com/segmentation/table/stroeh_mouse_retina",
            "shortlink_server" : None,
            "skeleton_source" : "precomputed://middleauth+https://minnie.microns-daf.com/skeletoncache/api/v1/stroeh_mouse_retina/precomputed/skeleton",
            "soma_table_format" : None,
            "soma_table_name" : None,
            "swamp_mesh_source" : None,
            "swamp_seg_ids": None,
            "synapse_table_format": None,
            "synapse_table_name": None,
            "tt_notes": "shortlink server may be may be https://spelunker.cave-explorer.org/#!middleauth+https://global.daf-apis.com/nglstate/api/v1/",
            "viewer_2d_zoom" : 1.6,
            "viewer_3d_angle" : [0, 0, 0, 1],
            "viewer_3d_zoom" : 93293,
            "viewer_res" : [16, 16, 40],
            "viewer_site" : "https://spelunker.cave-explorer.org",
            "viewer_start_coords" : [36501, 42459, 1032],
            "volume_size" : [81920, 81920, 2065],
            "volume_min_coord" : [0, 0, 0],
            "volume_max_coord" : [81919, 81919, 2064],
            "volume_center_coord": [40960, 40960, 1032],
            "whole_stack_mesh_source" : None,
            # --- unique entries below this line --- #
        },
        # last updated 2026/10/12
        "zheng_ca3" : {
            "alignment_cave_id": 12,
            "alignment_display_name": "Zheng CA3",           
            "alignment_description" : None,
            "alignment_name": "zheng_ca3",
            "cell_info_table_format" : None,
            "cell_info_table_name" : None,
            "dataset_name": "CA3",
            "datastack_description": None,
            "image_source" : "precomputed://gs://zheng_mouse_hippocampus_production/v2/img_aligned_sharded_18nm",
            "local_server" : "https://minnie.microns-daf.com",
            "neuropil_mesh_source" : None,
            "proofreading_table_format" : None,
            "proofreading_table_name" : None,
            "seg_source" : "graphene://middleauth+https://minnie.microns-daf.com/segmentation/table/zheng_ca3",
            "shortlink_server" : None,
            "skeleton_source" : "precomputed://middleauth+https://minnie.microns-daf.com/skeletoncache/api/v1/zheng_ca3/precomputed/skeleton",
            "soma_table_format" : None,
            "soma_table_name" : None,
            "swamp_mesh_source" : None,
            "swamp_seg_ids": None,
            "synapse_table_format": "syn_std", #CHECK#
            "synapse_table_name": "synapses_ca3_v1",
            "tt_notes": None,
            "viewer_2d_zoom" : 1.65,
            "viewer_3d_angle" : [0, 0, 0, 1],
            "viewer_3d_zoom" : 66402,
            "viewer_res" : [18, 18, 45],
            "viewer_site" : "https://spelunker.cave-explorer.org/",
            "viewer_start_coords" : [46221, 48531, 1119],
            "volume_size" : [51420, 57384, 2047],
            "volume_min_coord" : [20511, 19839, 96],
            "volume_max_coord" : [71931, 77223, 2143],
            "volume_center_coord": [46221, 48531, 1119],
            "whole_stack_mesh_source" : None,
            # --- unique entries below this line --- #
        },
        # template for adding new config dicts #
        # # last updated 
        # "name" : {
        #     "alignment_cave_id": 0,
        #     "alignment_display_name": "",
        #     "alignment_description" : "",
        #     "alignment_name": "",
        #     "cell_info_table_format" : "cell_std",
        #     "cell_info_table_name" : "",
        #     "dataset_name": "",
        #     "datastack_description": "",
        #     "image_source" : "",
        #     "local_server" : "",
        #     "neuropil_mesh_source" : "",
        #     "proofreading_table_format" : "proof_std",
        #     "proofreading_table_name" : "",
        #     "seg_source" : "",
        #     "shortlink_server" : "",
        #     "skeleton_source" : "",
        #     "soma_table_format" : "soma_std",
        #     "soma_table_name" : "",
        #     "swamp_mesh_source" : "",
        #     "swamp_seg_ids": [],
        #     "synapse_table_format": "syn_std",
        #     "synapse_table_name": "",
        #     "tt_notes": None,
        #     "viewer_2d_zoom" : 10,
        #     "viewer_3d_angle" : [0,0,0,1],
        #     "viewer_3d_zoom" : 10000,
        #     "viewer_res" : [],
        #     "viewer_site" : "",
        #     "viewer_start_coords" : [],
        #     "volume_size" : [],
        #     "volume_min_coord" : [],
        #     "volume_max_coord" : [],
        #     "volume_center_coord": [],
        #     "whole_stack_mesh_source" : "",
        #     # --- unique entries below this line --- #
        # },
    }

    # pulls the requested config dict value using name 
    # if it fails, returns error message 
    try:
        config = configs[datastack]
        return config
    except:
        print(
            f"No supported configs with the name {datastack} exist. For a list of all currently-supported configs, use the get_supported_configs() function."
        )
        return

def get_supported_configs():
    """
    Returns a list of names of all currently-supported CAVE datastacks with tracer configs.

    Not all configs have the same level of support.
    Check the individual dictionaries before assuming they'll work in all situations.

    Returns:
        config_names (list of str):
            the names of all the currenty-supported datastacks with config dictionaries
    """

    # makes list of config names
    config_names = [
        "basil-seg-aug"
        "brain_and_nerve_cord",
        "brain_and_nerve_cord_public",
        "fafb_v15_20221128025036",
        "fanc_production_mar2021",
        "fanc_sandbox",
        "flywire_fafb_production",
        "flywire_fafb_public",
        "flywire_fafb_sandbox",
        # "male_adult_nerve_cord"
        "minnie35_phase3_v0",
        "minnie35_public_v0",
        "minnie65_phase2_flat",
        "minnie65_phase3_v0",
        "minnie65_phase3_v1",
        "minnie65_public",
        "minnie65_sandbox",
        "mrgd",
        "pinky_sandbox",
        "stroeh_mouse_retina",
        "zheng_ca3",
    ]

    return config_names

def get_table_format_dict(table_format):
    """
    Gets the formatting dictionary for a datastack's backend table.

    Args:
        table_format (str):
            the name of the table format to get the dictionary for

    Returns:
        format_dict (dictionary):
            a dictionary containing the names of table columns for specific types of info
            e.g. the standard synapse table format "syn_std" uses the string "post_pt_root_id"
            for the column of postsynaptic segment IDs, keyed in the format dictionary as "post_seg"
    """
    
    # makes dict of all table format dicts
    full_dict = {
        # Standard Cell Info/ID Table
        "cell_std": {
            "coord": "pt_position",
            "created": "created",
            "id": "id",
            "seg": "pt_root_id",
            "superceded_id": "superceded_id",
            "sv": "pt_supervoxel_id",
            "tag_cols": ["tag","tag2"],
            "user_id": "user_id",
            "valid": "valid",
        },
        # Standard Proofreading Status Table
        "proof_std": {
            "coord": "pt_position",
            "created": "created",
            "id": "id",
            "proofread": "proofread",
            "seg": "pt_root_id",
            "superceded_id": "superceded_id",
            "sv": "pt_supervoxel_id",
            "user_id": "user_id",
            "valid": "valid",
            "valid_id": "valid_id",
        },
        # Standard Soma/Nuclei Table
        "soma_std": {
            "bb_end_coord": "bb_end_position",
            "bb_start_coord": "bb_start_position",
            "coord": "pt_position",
            "created": "created",
            "id": "id",
            "seg": "pt_root_id",
            "superceded_id": "superceded_id",
            "sv": "pt_supervoxel_id",
            "valid": "valid",
            "volume": "volume",
        },
        # Flywire Synapse Table
        # same as sstandard but with nt, connection, and cleft scores
        # no centerpoint
        "syn_flywire": {
            "connection_score": "connection_score",
            "cleft_score": "cleft_score",
            "center_coord": None,
            "created": "created",
            "id": "id",
            "nt_cols": ["ach", "da", "gaba", "glut", "oct", "ser"],
            "post_coord" : "post_pt_position",
            "post_seg" : "post_pt_root_id",
            "post_sv" : "post_pt_supervoxel_id",
            "pre_coord" : "pre_pt_position",
            "pre_seg" : "pre_pt_root_id",
            "pre_sv" : "pre_pt_supervoxel_id",
            "size": "size",
            "superceded_id": "superceded_id",
            "valid": "valid",
            "valid_nt": "valid_nt",
        },
        # Standard CAVE Synapse Table
        "syn_std": {
            "connection_score": None,
            "cleft_score": None,
            "center_coord": "ctr_pt_position",
            "created": "created",
            "id": "id",
            "nt_cols": None,
            "post_coord" : "post_pt_position",
            "post_seg" : "post_pt_root_id",
            "post_sv" : "post_pt_supervoxel_id",
            "pre_coord" : "pre_pt_position",
            "pre_seg" : "pre_pt_root_id",
            "pre_sv" : "pre_pt_supervoxel_id",
            "size": "size",
            "superceded_id": "superceded_id",
            "valid": "valid",
            "valid_nt": None,
        },
    }

    # handles bad input
    if table_format in full_dict:
        format_dict = full_dict[table_format]
        return format_dict
    else:
        print(table_format,"is not a valid table format. For a full list of all format types, use get_supported_table_formats().")

def get_supported_table_formats():
    """
    Returns an alphabetical list of supported table formats with brief descriptions as strings.
    
    Args:
        None

    Returns:
        table_format_list (list of strings):
            an alphabetical list of all the table format names with brief descriptions of their purpose
    """

    table_format_list = [
        "cell_std (The standard format for a cell information/identification table)",
        "proof_std (The standard format for a proofreading table)",
        "soma_std (The standard format for a soma/nucleus table)",
        "syn_flywire (The format for Flywire's synapse table, including neurotransmitters and cleft scores)",
        "syn_std (The standard format for a cell information/identification table)",
    ]

    return table_format_list