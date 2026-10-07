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
        # last updated 2026/10/7
        "brain_and_nerve_cord": {
            "cave_id": 9,
            "publisher_description" : 'The BANC (said "the bank") is the Brain And Nerve Cord, a GridTape transmission electron microscopy dataset of a female adult Drosophila melanogaster\'s entire central nervous system. Visit https://banc.community for more information.',
            "resolution": [4, 4, 45],
            "volume_size": [262144, 294912, 7010],
            "min_coord" : [0,0,0],
            "max_coord" : [262143, 294911, 7009],
            "center_coord": [131027, 147460, 3505],
            "em_source_url": "precomputed://gs://seunglab_lee_fly_cns_001_alignment/aligned/v0",
            "seg_source_url": "graphene://middleauth+https://cave.fanc-fly.com/segmentation/table/wclee_fly_cns_001",
            "skeleton_source_url": "precomputed://https://cave.fanc-fly.com/skeletoncache/api/v1/brain_and_nerve_cord/precomputed/skeleton",
            "synapse_table_name": "synapses_v2",
            "syn_pre_coord_col": "pre_pt_position",
            "syn_post_coord_col": "post_pt_position",
            "syn_pre_seg_col": "pre_pt_root_id",
            "syn_post_seg_col": "post_pt_root_id",
            "syn_pre_sv_col": "pre_pt_supervoxel_id",
            "syn_post_sv_col": "post_pt_supervoxel_id",
            "syn_nt_cols": None,
            "syn_cleft_score_col": None,
            "cell_info_table_name": "cell_info",
            "soma_table_name": None,
            "proofreading_table_name": "backbone_proofread",
            "proofreading_table_seg_col": "pt_root_id",
            "proofreading_table_status_col": "proofread",
            "local_server_url": "https://cave.fanc-fly.com",
            "viewer_site_url": "https://spelunker.cave-explorer.org/",
            "main_stack_mesh_url": "precomputed://gs://lee-lab_brain-and-nerve-cord-fly-connectome/region_outlines",
            "neuropil_mesh_url": None,
            "default_view_point": [125563, 118181, 2850],
            "default_zoom_2d": 4.12,
            "default_zoom_3d": 360849,
            "default_angle_3d": [0, 1, 0, 0],
            "shortlink_server_url": None,
            "swamp_source_url": "https://c10s.pni.princeton.edu/tracers/swamps/banc/main|neuroglancer-precomputed:",
            "swamp_ids": [1,2,3,4,5,6,7,8,9,10,11],
            # --- unique entries below this line --- #
            # hosting url for MANC datastack aligned comparison mesh
            "manc_seg_source_url": "precomputed://gs://lee-lab_brain-and-nerve-cord-fly-connectome/imported_meshes/manc_v1.2.1_meshes_elastix_tpsreg_240721",
        },
        # last updated 2026/10/7
        "flywire_fafb_production": {
            "cave_id": 2,
            "publisher_description" : "The seung lab's realignment of the FAFB dataset",
            "resolution": [4, 4, 40],
            "volume_size": [270336, 147456, 7062], # estimated #
            "min_coord" : [0,0,0],
            "max_coord" : [270335, 147455, 7061], # estimated #
            "center_coord": [135168, 73728, 3531], # estimated #
            # old "em_source_url": "precomputed://https://bossdb-open-data.s3.amazonaws.com/flywire/fafbv14",
            "em_source_url": "precomputed://gs://flywire_em/aligned/v1",
            "seg_source_url": "graphene://https://prodv1.flywire-daf.com/segmentation/1.0/fly_v31",
            "skeleton_source_url": "precomputed://https://prod.flywire-daf.com/skeletoncache/api/v1/flywire_fafb_production/precomputed/skeleton",
            "synapse_table_name": "synapses_nt_v1",
            "syn_pre_coord_col": "pre_pt_position",
            "syn_post_coord_col": "post_pt_position",
            "syn_pre_seg_col": "pre_pt_root_id",
            "syn_post_seg_col": "post_pt_root_id",
            "syn_pre_sv_col": "pre_pt_supervoxel_id",
            "syn_post_sv_col": "post_pt_supervoxel_id",
            "syn_nt_cols": ["ach", "da", "gaba", "glut", "oct", "ser"],
            "syn_cleft_score_col": "cleft_score",
            "cell_info_table_name": "neuron_information_v2",
            "soma_table_name": "nuclei_v1",
            "proofreading_table_name": "proofreading_status_public_v1",
            "proofreading_table_seg_col": "pt_root_id",
            "proofreading_table_status_col": "proofread",
            "local_server_url": "https://prod.flywire-daf.com",
            "viewer_site_url": "https://ngl.flywire.ai/",
            "main_stack_mesh_url": "precomputed://gs://flywire_neuropil_meshes/whole_neuropil/brain_mesh_v141.surf",
            "neuropil_mesh_url": "precomputed://gs://flywire_neuropil_meshes/neuropils/neuropil_mesh_v141_v3",
            "default_view_point": [131071, 147456, 3505],
            "default_zoom_2d": 13.2,
            "default_zoom_3d": 9600,
            "default_angle_3d": [0, 0, 0, -1],
            "shortlink_server_url": "https://globalv1.flywire-daf.com/nglstate/post",
            "swamp_source_url": None,
            "swamp_ids": None,
            # --- unique entries below this line --- #
            # proofreading review table
            "proofreading_review_table_name": "proofreading_review_public_v1",
        },
        # last updated 2026/10/7
        "male_adult_nerve_cord": {
            "cave_id": None,
            "publisher_description" : None,
            "resolution": [8, 8, 8],
            "volume_size": [],
            "min_coord" : [],
            "max_coord" : [],
            "center_coord": [],
            "em_source_url": "precomputed://gs://flyem-vnc-2-26-213dba213ef26e094c16c860ae7f4be0/v3_emdata_clahe_xy/jpeg",
            "seg_source_url": "precomputed://gs://manc-seg-v1p2/manc-seg-v1.2",
            "skeleton_source_url": None,
            "synapse_table_name": None,
            "syn_pre_coord_col": None,
            "syn_post_coord_col": None,
            "syn_pre_seg_col": None,
            "syn_post_seg_col": None,
            "syn_pre_sv_col": None,
            "syn_post_sv_col": None,
            "syn_nt_cols": None,
            "syn_cleft_score_col": None,
            "cell_info_table_name": None,
            "soma_table_name": None,
            "proofreading_table_name": None,
            "proofreading_table_seg_col": None,
            "proofreading_table_status_col": None,
            "local_server_url": None,
            "viewer_site_url": None,
            "main_stack_mesh_url": "precomputed://gs://flyem-vnc-roi-d5f392696f7a48e27f49fa1a9db5ee3b/all-vnc-roi",
            "neuropil_mesh_url": "precomputed://gs://flyem-vnc-roi-d5f392696f7a48e27f49fa1a9db5ee3b/roi-202208",
            "default_view_point": None,
            "default_zoom_2d": 10,
            "default_zoom_3d": 10000,
            "default_angle_3d": [0, 0, 0, 0],
            "shortlink_server_url": None,
            "swamp_source_url": None,
            "swamp_ids": None,
            # --- unique entries below this line --- #
            # mesh of nerve bundles #
            "nerve_mesh_source_url": "precomputed://gs://flyem-vnc-roi-d5f392696f7a48e27f49fa1a9db5ee3b/nerve-roi-202301",
            # annotation layer for presynaptic points #
            "presyn_anno_layer_source_url": "precomputed://gs://manc-seg-v1p2/manc-v1.2-synapse-partners-minconf-0.0.precomputed",
            # annotation layer for postsynaptic points #
            "postsyn_anno_layer_source_url": "precomputed://gs://manc-seg-v1p2/manc-v1.2-synapse-partners-minconf-0.0.precomputed",
        },
        # last updated 2026/10/7
        "minnie65_phase3_v1" : {
            "cave_id": 1,
            "publisher_description" : "This is the second alignment of the IARPA 'minnie65' dataset, completed in the spring of 2020 that used the seamless approach. This is the first version of Minnie that has proofreading enabled. Was first enabled on June 24, 2020.",
            "resolution" : [4,4,40],
            "volume_size" : [384848, 262102, 13008],
            "min_coord" : [52770,60616,14850],
            "max_coord" : [437618,322718,27858],
            "center_coord": [245194, 191667, 21354],
            "em_source_url" : "precomputed://https://bossdb-open-data.s3.amazonaws.com/iarpa_microns/minnie/minnie65/em",
            "seg_source_url" : "graphene://middleauth+https://minnie.microns-daf.com/segmentation/table/minnie3_v1",
            "skeleton_source_url" : "precomputed://middleauth+https://minnie.microns-daf.com/skeletoncache/api/v1/minnie65_phase3_v1/precomputed/skeleton",
            "synapse_table_name" : "synapses_pni_2",
            "syn_pre_coord_col" : "pre_pt_position",
            "syn_post_coord_col" : "post_pt_position",
            "syn_pre_seg_col" : "pre_pt_root_id",
            "syn_post_seg_col" : "post_pt_root_id",
            "syn_pre_sv_col" : "pre_pt_supervoxel_id",
            "syn_post_sv_col" : "post_pt_supervoxel_id",
            "syn_nt_cols" : None,
            "syn_cleft_score_col" : None,
            "cell_info_table_name" : None,
            "soma_table_name" : "nucleus_neuron_svm",
            "proofreading_table_name" : None,
            "proofreading_table_seg_col" : None,
            "proofreading_table_status_col" : None,
            "local_server_url" : "https://minnie.microns-daf.com",
            "viewer_site_url" : "https://spelunker.cave-explorer.org/",
            "main_stack_mesh_url" : None,
            "neuropil_mesh_url" : None,
            "default_view_point" : [245194, 191667, 21354],
            "default_zoom_2d" : 3,
            "default_zoom_3d" : 1215104,
            "default_angle_3d" : [0,0,0,0],
            "shortlink_server_url" : None,
            "swamp_source_url" : None,
            "swamp_ids": None,
            # --- unique entries below this line --- #
        },
        # last updated 2026/10/7
        "mrgd" : {
            "cave_id": 10,
            "publisher_description" : "Mouse dorsal spine",
            "resolution" : [4,4,45],
            "volume_size" : [201727, 82943, 498],
            "min_coord" : [0,0,0],
            "max_coord" : [201727, 82943, 498],
            "center_coord": [100863, 41471, 249],
            "em_source_url" : "precomputed://gs://zetta_lee_mouse_spinal_cord_001_image/dorsal_sections/dorsal_sections_500_jpeg",
            "seg_source_url" : "graphene://https://cave.fanc-fly.com/segmentation/table/mouse_dorsal_spine",
            "skeleton_source_url" : None,
            "synapse_table_name" : None,
            "syn_pre_coord_col" : None,
            "syn_post_coord_col" : None,
            "syn_pre_seg_col" : None,
            "syn_post_seg_col" : None,
            "syn_pre_sv_col" : None,
            "syn_post_sv_col" : None,
            "syn_nt_cols" : None,
            "syn_cleft_score_col" : None,
            "cell_info_table_name" : None,
            "soma_table_name" : None,
            "proofreading_table_name" : None,
            "proofreading_table_seg_col" : None,
            "proofreading_table_status_col" : None,
            "local_server_url" : "https://cave.fanc-fly.com",
            "viewer_site_url" : "https://neuromancer-seung-import.appspot.com",
            "main_stack_mesh_url" : None,
            "neuropil_mesh_url" : None,
            "default_view_point" : [100863, 41471, 249],
            "default_zoom_2d" : 8,
            "default_zoom_3d" : 14764,
            "default_angle_3d" : [0,0,0,1],
            "shortlink_server_url" : None,
            "swamp_source_url" : None,
            "swamp_ids": None,
            # --- unique entries below this line --- #
        },
        # last updated 2026/10/7
        "stroeh_mouse_retina": {
            "cave_id": 14,
            "publisher_description" : None,
            "resolution": [16, 16, 40],
            "volume_size": [81920,81920,2065], # estimated #
            "min_coord" : [0,0,0],
            "max_coord" : [81919, 81919, 2064], # estimated #
            "center_coord": [40960,40960, 1032], # estimated #
            "em_source_url": "precomputed://gs://stroeh_sem_mouse_retina/image/v2",
            "seg_source_url": "graphene://middleauth+https://minnie.microns-daf.com/segmentation/table/stroeh_mouse_retina",
            "skeleton_source_url": "precomputed://middleauth+https://minnie.microns-daf.com/skeletoncache/api/v1/stroeh_mouse_retina/precomputed/skeleton",
            "synapse_table_name": None,
            "syn_pre_coord_col": None,
            "syn_post_coord_col": None,
            "syn_pre_seg_col": None,
            "syn_post_seg_col": None,
            "syn_pre_sv_col": None,
            "syn_post_sv_col": None,
            "syn_nt_cols": None,
            "syn_cleft_score_col": None,
            "cell_info_table_name": None,
            "soma_table_name": None,
            "proofreading_table_name": None,
            "proofreading_table_seg_col": None,
            "proofreading_table_status_col": None,
            "local_server_url": "https://minnie.microns-daf.com",
            "viewer_site_url": "https://spelunker.cave-explorer.org",
            "main_stack_mesh_url": None,
            "neuropil_mesh_url": None,
            "default_view_point": [36501, 42459, 1032],
            "default_zoom_2d": 1.6,
            "default_zoom_3d": 93293,
            "default_angle_3d": [0, 0, 0, 1],
            "shortlink_server_url": None,  # may be https://spelunker.cave-explorer.org/#!middleauth+https://global.daf-apis.com/nglstate/api/v1/ #
            "swamp_source_url": None,
            "swamp_ids": None,
            # --- unique entries below this line --- #
        },
        # last updated 2026/10/7
        "zheng_ca3" : {
            "cave_id": 12,
            "publisher_description" : None,
            "resolution" : [18,18,45],
            "volume_size" : [51420, 57384, 2047], # estimated #
            "min_coord" : [20511, 19839, 96], # estimated #
            "max_coord" : [71931, 77223, 2143], # estimated #
            "center_coord": [46221, 48531, 1119], # estimated #
            "em_source_url" : "precomputed://gs://zheng_mouse_hippocampus_production/v2/img_aligned_sharded_18nm",
            "seg_source_url" : "graphene://middleauth+https://minnie.microns-daf.com/segmentation/table/zheng_ca3",
            "skeleton_source_url" : "precomputed://middleauth+https://minnie.microns-daf.com/skeletoncache/api/v1/zheng_ca3/precomputed/skeleton",
            "synapse_table_name" : "synapses_ca3_v1",
            "syn_pre_coord_col" : "pre_pt_position",
            "syn_post_coord_col" : "post_pt_position",
            "syn_pre_seg_col" : "pre_pt_root_id",
            "syn_post_seg_col" : "post_pt_root_id",
            "syn_pre_sv_col" : "pre_pt_supervoxel_id",
            "syn_post_sv_col" : "post_pt_supervoxel_id",
            "syn_nt_cols" : None,
            "syn_cleft_score_col" : None,
            "cell_info_table_name" : None,
            "soma_table_name" : None,
            "proofreading_table_name" : None,
            "proofreading_table_seg_col" : None,
            "proofreading_table_status_col" : None,
            "local_server_url" : "https://minnie.microns-daf.com",
            "viewer_site_url" : "https://spelunker.cave-explorer.org/",
            "main_stack_mesh_url" : None,
            "neuropil_mesh_url" : None,
            "default_view_point" : [46221, 48531, 1119],
            "default_zoom_2d" : 1.65,
            "default_zoom_3d" : 66402,
            "default_angle_3d" : [0,0,0,0],
            "shortlink_server_url" : None,
            "swamp_source_url" : None,
            "swamp_ids": None,
            # --- unique entries below this line --- #
        },
        # # template for adding new config dicts #
        # "name" : {
        #     "cave_id": 0,
        #     "publisher_description" : "",
        #     "resolution" : [],
        #     "volume_size" : [],
        #     "min_coord" : [],
        #     "max_coord" : [],
        #     "center_coord": [],
        #     "em_source_url" : "",
        #     "seg_source_url" : "",
        #     "skeleton_source_url" : "",
        #     "synapse_table_name" : "",
        #     "syn_pre_coord_col" : "",
        #     "syn_post_coord_col" : "",
        #     "syn_pre_seg_col" : "",
        #     "syn_post_seg_col" : "",
        #     "syn_pre_sv_col" : "",
        #     "syn_post_sv_col" : "",
        #     "syn_nt_cols" : [],
        #     "syn_cleft_score_col" : "",
        #     "cell_info_table_name" : "",
        #     "soma_table_name" : "",
        #     "proofreading_table_name" : "",
        #     "proofreading_table_seg_col" : "",
        #     "proofreading_table_status_col" : "",
        #     "local_server_url" : "",
        #     "viewer_site_url" : "",
        #     "main_stack_mesh_url" : "",
        #     "neuropil_mesh_url" : "",
        #     "default_view_point" : [],
        #     "default_zoom_2d" : 10,
        #     "default_zoom_3d" : 10000,
        #     "default_angle_3d" : [0,0,0,0],
        #     "shortlink_server_url" : "",
        #     "swamp_source_url" : "",
        #     "swamp_ids": [],
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
        "brain_and_nerve_cord",
        "flywire_fafb_production",
        "male_adult_nerve_cord (not CAVE-supported, incomplete)",
        "minnie65_phase3_v1 (linkbuilder currently has bug with 3d rotation failing)",
        "mrgd",
        "stroeh_mouse_retina",
        "zheng_ca3 (linkbuilder currently has bug with 3d rotation failing)"
    ]

    return config_names