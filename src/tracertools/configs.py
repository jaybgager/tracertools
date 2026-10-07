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
        "brain_and_nerve_cord": {
            "resolution": [4, 4, 45],
            "volume_size": [262144, 294912, 7010],
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
            # unique entries below this line #
            "manc_seg": "precomputed://gs://lee-lab_brain-and-nerve-cord-fly-connectome/imported_meshes/manc_v1.2.1_meshes_elastix_tpsreg_240721",
        },
        "flywire_fafb_production": {
            "resolution": [4, 4, 40],
            "volume_size": [],
            "em_source_url": "precomputed://https://bossdb-open-data.s3.amazonaws.com/flywire/fafbv14",
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
            "proofreading_table_name": "proofreading_status_public_v1",  # there's also "proofreading_review_public_v1" #
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
        },
        "male_adult_nerve_cord": {
            "resolution": [8, 8, 8],
            "volume_size": [],
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
            # unique entries below this line #
            "nerve_mesh_url": "precomputed://gs://flyem-vnc-roi-d5f392696f7a48e27f49fa1a9db5ee3b/nerve-roi-202301",
            "presyn_anno_layer": "precomputed://gs://manc-seg-v1p2/manc-v1.2-synapse-partners-minconf-0.0.precomputed",
            "postsyn_anno_layer": "precomputed://gs://manc-seg-v1p2/manc-v1.2-synapse-partners-minconf-0.0.precomputed",
        },
        "stroeh_mouse_retina": {
            "resolution": [16, 16, 40],
            "volume_size": [],
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
        },
        # # template for adding new config dicts #
        # "name" : {
        #     "resolution" : [],
        #     "volume_size" : [],
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
        "male_adult_nerve_cord",
        "stroeh_mouse_retina",
    ]

    return config_names