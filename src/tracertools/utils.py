from caveclient import CAVEclient
from cloudfiles import CloudFiles
import cloudvolume
from collections import Counter
import datetime
import gspread
import json
import microviewer
from nglui.statebuilder import *
import numpy as np
import os
from osteoid import Skeleton
import pandas as pd
from pathlib import Path
import platform
import plotly.graph_objects as go
from scipy.spatial import Delaunay, cKDTree
import statistics
import sys
import time
from tqdm import tqdm
import trimesh
from urllib.error import HTTPError
from urllib.parse import quote


def bucket_convert_colons(
    file_path, 
    to_windows=True,
):
    """
    Converts file names with colons to Windows-valid format and back.

    Used primarily for working with legacy-format single-resolution NG meshes,
    which require certain files to have colons in their names.
    
    Args:
        file_path (str):
            the file path you want to convert
        to_windows (bool, optional, default=True):
            if True, converts colons in name to windows-valid placeholder '___'
            if False, converts placeholders '___' back to colons

    Returns:
        output_file_path (str):
            the converted file path
    """

    # handles behavior for converting TO Windows
    if to_windows == True:
        output_file_path = file_path.replace(":", "___")
    
    # handles behavior for converting FROM Windows
    elif to_windows == False:
        output_file_path = file_path.replace("___", ":")
    
    # handles non-bool input for to_windows parameter
    else:
        raise TypeError(
            f"The 'to_windows' argument must be True or False, not {type(to_windows)}"
        )

    return output_file_path


def bucket_delete_file(file_path):
    """
    Deletes a file on a cloudfiles-managed bucket.

    Args:
        file_path (str):
            the absolute filepath to the file you want to delete on the bucket
    """

    # splits file_path into file name and folder path
    split_path = list(file_path.rpartition("/"))

    # sets folder and file name variables
    folder_path, file_name = split_path[0], split_path[2]

    # creates CloudFiles object using folder path
    cf = CloudFiles(folder_path)

    # deletes file with file name in folder
    cf.delete(file_name)


def bucket_delete_folder(folder_path):
    """
    Deletes an entire folder from a cloudfiles-managed bucket.

    Requires write access for the selected bucket.
    Use caution, as this can delete an entire bucket
    if the root directory is passed as the folder_path.

    Args:
    folder_path (str):
        the absolute path to the folder you want to delete on the bucket
    """

    # creates cloudfile object of bucket folder
    cf = CloudFiles(folder_path)

    # gets length of deletion list 
    item_number = len(list(cf))

    # double-checks that the user wants to delete a whole folder
    check = input(
        f"!!!WARNING!!! Are you sure you want to delete the entire folder {folder_path} and all {item_number} files contained within it? If so, type 'delete' and hit enter."
    )

    # deletes if check passed, prints descriptive message in either case
    if check == "delete":
        
        # iterates through items in folder, deleting each #
        for i in list(cf):
            cf.delete(i)
        
        print()
        print("Folder {folder_path} and all its contents have been deleted.")
        print()
    
    else:
        print()
        print("Folder was not deleted.")
        print()


def bucket_download_file(
    bucket_path, 
    download_path=None,
):
    """
    Downloads a file from a cloudfiles-managed bucket.

    Args:
        bucket_path (str):
            the absolute filepath of the file in the bucket
        download_path (str, optional, default=None):
            the absolute path to the folder on your local machine 
            where you want the downloaded file to go 
            if None, tries to find default "Downloads" folder
    """

    # tries to get the user's Downloads folder path if none specified
    if download_path == None:
        try:
            download_path = str(Path.home() / "Downloads")
        except:
            raise Exception(
                "Default download folder couldn't be found, please specify the absolute file path to a folder using the 'download_folder' argument."
            )

    # splits file name and folder path into list
    split_path = list(bucket_path.rpartition("/"))

    # sets individual folder and file name variables
    folder_path, file_name = split_path[0],split_path[2]

    # creates cloudfiles object using bucket path
    cf = CloudFiles(folder_path)

    # gets content of file using name
    file_contents = cf.get([file_name])

    # removes trailing slash from download folder path if present
    if download_path[-1] == "/":
        download_path = download_path[:-1]

    # sets timestamp for unique file name
    timestamp = datetime.datetime.now().strftime("_%Y_%m_%d_%H%M%S")

    # converts file names with colons into windows-valid format
    # replaces colons with triple underscore ___
    if platform.system() == "Windows":
        file_name = bucket_convert_colons(file_path=file_name,to_windows=True)

    # sets download path and file name
    download_path = download_path + "/" + file_name + timestamp

    # creates file by feeding path with name and contents into pathlib
    dl = Path(download_path)

    # writes the file data to the specified lcoation
    dl.write_bytes(file_contents[0]["content"])


def bucket_download_folder(
    bucket_path, 
    download_path=None,
):
    """
    Downloads a folder from a cloudfiles-managed bucket.

    Args:
        bucket_path (str):
            the absolute filepath of the bucket folder you want to download (str)
        download_path (str, optional, default=None):
            the absolute path to the folder on your local machine 
            where you want the downloaded folder to go 
            if None, tries to find default "Downloads" folder
    """

    # tries to get the user's Downloads folder path if none specified 
    if download_path == None:
        try:
            download_path = str(Path.home() / "Downloads")
        except:
            raise Exception(
                "Default download folder couldn't be found, please specify the absolute file path to a folder using the 'download_folder' argument."
            )

    # removes trailing slash from dl folder path if present 
    if download_path[-1] == "/":
        download_path = download_path[:-1]

    # removes trailing slash from bucket path if present 
    if bucket_path[-1] == "/":
        bucket_path = bucket_path[:-1]

    # splits file name and folder path into list 
    split_path = list(bucket_path.rpartition("/"))

    # removes slash delimiter from list #
    del split_path[1]

    # sets path of directory folder is in and folder name variables 
    dir_path, folder_name = split_path

    # creates cloudfile object of bucket folder
    cf = CloudFiles(bucket_path)

    # creates empty list to fill with file dicts 
    file_dict_list = []

    # creates dict of file name and info for each in bucket folder and adds to list 
    for i in list(cf):
        if i[-3:] == ".gz":
            file_dict = cf.get([i], raw=True)[0]
        else:
            file_dict = cf.get([i])[0]

        # converts file names with colons into Windows-valid format
        # by replacing colons with triple underscore ___
        if platform.system() == "Windows":
            file_dict["path"] = bucket_convert_colons(file_path=file_dict["path"], to_windows=True)

        file_dict_list.append(file_dict)

    # sets timestamp for unique folder name
    timestamp = datetime.datetime.now().strftime("_%Y_%m_%d_%H%M%S")

    # sets actual ouput path using dl folder path, bucket folder name, and timestamp
    output_path = download_path + "/" + folder_name + timestamp + "/"

    # downloads each file in the bucket folder to the appropriate local directory one by one
    # creates new directories where necessary
    for i in file_dict_list:
        fp = Path(output_path + i["path"])
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_bytes(i["content"])


def bucket_move_file(
    file_path, 
    new_folder_path,
):
    """
    Moves a file between two folders on a cloudfiles-managed bucket.

    Requires write access for the selected bucket.

    Args:
        file_path (str):
            the current absolute path on the bucket to the file you want to move
        new_folder_path (str):
            the new absolute path on the bucket to the folder you want to move the file to 
            will create new folders if they don't already exist
    """

    # splits file name and folder path into list 
    split_path = list(file_path.rpartition("/"))

    # sets individual folder and file name variables 
    folder_path, file_name = split_path[0],split_path[2]

    # removes trailing slash from new folder path if present 
    if new_folder_path[-1] == "/":
        new_folder_path = new_folder_path[:-1]

    # creates new path from new folder path and file name 
    new_path = new_folder_path + "/" + file_name

    # creates cloudfiles object from folder path 
    cf = CloudFiles(folder_path)

    # moves file from old location to new 
    cf.move(file_name, new_path)


def bucket_rename_file(
    file_path, 
    new_name,
):
    """
    Renames a file on a cloudfiles-managed bucket.

    Requires write access for the selected bucket.

    Args:
        file_path (str):
            the absolute path to the file on the bucket you want to rename
        new_name (str):
            the new name you want to give the file
            should include file extension if one was present in original
    """

    # splits file name and folder path into list
    split_path = list(file_path.rpartition("/"))

    # sets individual folder and file name variables
    folder_path, file_name = split_path[0],split_path[2]

    # creates new path string
    new_path = folder_path + "/" + new_name

    # skips identical paths
    if new_path == file_path:
        return

    # creates cloudfiles object from folder path
    cf = CloudFiles(folder_path)

    # "renames" file by moving it in place with a new path
    cf.move(file_name, new_path)


def bucket_upload_file(
    local_path, 
    bucket_path,
):
    """
    Adds a local file to a folder on a cloudfiles-managed bucket.
    
    Requires write access for the selected bucket.

    Args:
        local_path (str):
            the absolute path on your local machine to the file you want to upload
        bucket_path (str):
            the absolute path to the bucket folder you want to put the file in
            will create new folders where necessary
    """

    # if windows detected, replaces backslashes with forward
    if platform.system() == "Windows":
        local_path = local_path.replace("\\", "/")
    # if not windows, ensures local path starts with slash
    else:
        # adds leading slash if not present
        if local_path[0] != "/":
            local_path = "/" + local_path

    # removes trailing slash from bucket path if present 
    if bucket_path[-1] == "/":
        bucket_path = bucket_path[:-1]

    # gets file content
    try:
        with open(local_path, "r") as f:
            content = f.read()
    
    # handles binary files
    except UnicodeDecodeError:
        with open(local_path, "rb") as f:
            content = f.read()

    # creates a cloudfiles object using the bucket address
    bucket_cf = CloudFiles(bucket_path)

    # gets file name
    fname = local_path.rpartition("/")[-1]

    # uploads file to bucket 
    bucket_cf.put(fname, content)

    # converts Windows-valid triple underscore back to colons if necessary
    # by moving in place to rename on bucket (can't be done on local machine)
    if platform.system() == "Windows":
        fixed_fname = bucket_convert_colons(file_path=fname, to_windows=False)
        fixed_path = bucket_path + "/" + fixed_fname
        bucket_cf.move(fname, fixed_path)


def bucket_upload_folder(
    local_path, 
    bucket_path,
):
    """
    Copies a folder and its contents from a local machine to a folder on a cloudfiles-hosted bucket.

    Requires write access for the selected bucket.

    Args:
        local_path (str):
            the absolute path on your local machine to the folder that you want to upload
        bucket_path (str):
            the absolute path on the bucket to the folder where you want to upload the folder from 
            your local machine, including the name you want to give to the folder on the bucket.
            e.g. if you want to put a folder called 'image' from your local machine into the 
            bucket directory '/bucket/volumes' you would set this to '/bucket/volumes/image' 
            you don't have to use the same name as the folder being uploaded, this will rename it.
            will create new bucket folders where necessary
    """

    # removes trailing slash from bucket path if present
    if bucket_path[-1] == "/":
        bucket_path = bucket_path[:-1]

    # removes trailing slash from folder path if present 
    if local_path[-1] == "/":
        local_path = local_path[:-1]

    # sets destination folder
    cf_dest = CloudFiles(bucket_path)

    # transfers files from local folder to destination folder on bucket
    cf_dest.transfer_from(local_path)

    # fixes windows-formatted mesh file paths
    if platform.system() == "Windows":
        # for each file in the uploaded folder, renames if needed
        for fpath in list(cf_dest):
            if "___" in fpath:
                # replaces windows-valid triple underscores with ng-necessary colons in filenames
                full_path = bucket_path + "/" + fpath
                fname = list(full_path.rpartition("/"))[-1]
                fixed_path = bucket_convert_colons(file_path=full_path, to_windows=False)
                cf_dest.move(fpath, fixed_path)

def calc_3d_distance(
    point_a, 
    point_b, 
    res,
):
    """
    Calculates the 3D distance between two points in nanometers.

    Args:
        point_a (list of 3 ints):
            xyz coordinates of first point e.g. [1,2,3]
        point_b (list of 3 ints)
            xyz coordinates of second point e.g. [4,5,6]
        res (list of 3 ints):
            the nanometers per voxel in the x, y, and z directions that the coordinate system 
            you're working in uses e.g. [4,4,45]

    Returns:
        distance (float):
            the 3D distance in nanometers between points a and b
    """

    # calculates distance in x, y, and z dimensions individually
    x_dist = (res[0] * point_a[0]) - (res[0] * point_b[0])
    y_dist = (res[1] * point_a[1]) - (res[1] * point_b[1])
    z_dist = (res[2] * point_a[2]) - (res[2] * point_b[2])

    # uses distance formula to calculate distance in 3D
    distance = ((x_dist**2) + (y_dist**2) + (z_dist**2)) ** 0.5

    return distance

def calc_avg_point_coords(
    points, 
    exact_value=False,
):
    """
    Calculates the average point coordinates for a list of points.

    Although written for use with cartesian coordinates, this function 
    should work for coordinate systems with any number of dimensions.

    Args:
        points (list of lists of ints or floats):
            a list of point coordinate lists, e.g. [[X1,Y1,Z1],[X2,Y2,Z2],[X3,Y3,Z3]]
        exact_value (bool, optional, default=False):
            if True, will return results as exact floats instead of rounding to ints

    Returns:
        avg_point (list of ints)
            the average values for all the coords in the list, e.g. [Xavg,Yavg,Zavg] (list of ints)
    """

    # makes df using coords as columns
    df = pd.DataFrame(points)

    # calculates row means (e.g. average x, y, and z coordinates)
    raw_point_means = df.mean()

    # calculates means for each coordinate
    avg_point = raw_point_means.values.tolist()

    # rounds result to nearest integer if not asked for exact results
    if exact_value == False:
        avg_point = list(map(round, avg_point))

    return avg_point


def calc_bbox_corners_from_center(
    center_point, 
    dims,
):
    """
    Calculates the corner points of a bounding box using dimensions and a center point.

    Args:
        center_point (list of ints)
            point coordinates in voxels for the center of the bounding box
            e.g. [1,2,3]
        dims (list of 3 ints)
            desired bbox dimensions in voxels
            rounds numbers down to nearest even int to ensure true centering
            e.g. [100,100,10]

    Returns:
        corners (list of lists of ints):
            coordinates of corner points for bbox (list of lists of ints)
            e.g. [[1,2,3],[4,5,6]]
    """

    # ensures starting dims are even numbers
    for dim in dims:
        if dim % 2 != 0:
            dim += 1

    # creates empty lists
    min_point = [int(coord - dim / 2) for coord, dim in zip(center_point, dims)]
    max_point = [int(coord + dim / 2) for coord, dim in zip(center_point, dims)]

    # builds corners list from min and max points
    corners = [min_point, max_point]

    return corners

def calc_line_triangle_intersect(
    line, 
    triangle,
    precision=0
):
    """
    Calculates the intersection point, if any, of a line segment and a triangular plane.

    Args:
        line ((2,3)-shape numpy array of floats):
            the point coords of the line segment's ends 
            e.g. [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]] 
        triangle ((3,3)-shape array of floats):
            a 2D array of shape (3,3) for the point coords of a triangle 
            e.g.[[1.0, 2.0, 3.0], [4.0 ,5.0, 6.0], [7.0, 8.0, 9.0]] 
        precision (int, optional, default=0):
            how precise to be when calculating intersection points
            specifically, maximum number of decimal points to include when rounding results
            default 0 rounds to nearest integer as this is fine for most neuroglancer uses
            using high precision (e.g 16+ digits) with small coord values (e.g. [1,1,1] 
            for coordinates can result in false negative results, as the float math involved 
            sometimes produces very tiny discrepancies when checking results

    Returns:
        result ((3)-shape numpy array of floats or None):
            if an intersection point was found, returns as array of floats
            otherwise returns None
    """

    # defines function for checking half of each line as a ray
    # breaks line into two opposing rays for math to work
    # then checks if each ray passes thought triangle individually
    # if both do, then intersection point is returned
    def _calc_ray_triangle_intersect(
        ray_origin, 
        ray_direction, 
        triangle,
    ):
        """
        Calculates the intersection point, if any, of a ray and a triangular plane.
        
        Uses Möller-Trumbore intersection algorithm.
        Ray and triangle point coordinates must be in the same voxel resolution.

        Args:
            ray_origin ((3)-shape numpy array of floats):
                the point coordinates where the ray begins 
            ray_direction ((3)-shape numpy array of floats):
                a vector representing the direction of the ray
                can be calculated by subtracting the point coords of the origin 
                from the point coords anywhere along the ray
            triangle ((3,3)-shape array of floats):
                point coordinates of the triangle's veritices 

        Returns:
            intersection_point ((3)-shape numpy array or None):
                the xyz coordinates where the ray and triangle intersect, or None if none exist
        """

        # splits triangle into individual vertex coord lists 
        v0, v1, v2 = triangle

        # unclear what this does 
        epsilon = 1e-8

        # gets edge vectors (x,y,and z distances) for two sides of triangle 
        edge1 = v1 - v0
        edge2 = v2 - v0

        # sets 'h' equal to the cross product of ray direction vector and the second edge vector 
        h = np.cross(ray_direction, edge2)

        # sets 'a' equal to the dot product of the first edge vector and h 
        a = np.dot(edge1, h)

        # if absolute value of a is less than epsilon, ray is parallel to triangle 
        # I think this whole section ultimately checks the dot product of the 
        # ray's direction vector and triangle's normal vector to see if they're zero?
        # this indicates ray is parallel to triangle 
        if abs(a) < epsilon:
            return None

        # I think this following section uses something called barycentric coordinates 
        # to determine the point of intersection between the ray and the plane 
        # the triangle is on, but I'm not sure how #

        # sets 'f' equal to the reciprocal of 'a'
        f = 1.0 / a

        # sets 's' equal to a distance vector between 
        # the ray origin and the first point on the triangle 
        s = ray_origin - v0

        # sets 'u' equal to the dot product of 's' and 'h' times the reciprocal of 'a'
        u = f * np.dot(s, h)

        # checks if u is between 0 and 1, unsure why 
        if u < 0.0 or u > 1.0:
            return None

        # sets 'q' equal to cross product of (distance vector between ray origin and 
        # first triangle point) and (edge length of first side of triangle)
        q = np.cross(s, edge1)

        # sets 'v' equal to reciprocal of 'a' times dot product of ray direction vector and 'q' 
        v = f * np.dot(ray_direction, q)

        # if 'v' is less than 0 or sum of 'u' and 'v' is over 1, no intersection 
        # unclear why 
        if v < 0.0 or u + v > 1.0:
            return None

        # sets 't' to reciprocal of 'a' times dot product of second triangle edge length and 'q' 
        t = f * np.dot(edge2, q)

        # if 't' is greater than epsilon value, calculates the intersection point of the ray 
        # and triangle by multiplying ray direction vector by 't' and adding to origin point 
        if t > epsilon:
            intersection_point = ray_origin + ray_direction * t
            return intersection_point

        # if 't' is less than or equal to epsilon, no intersection 
        return None

    # sets ray origin points 
    ray_origin_1 = line[0]
    ray_origin_2 = line[1]

    # creates ray direction vectors in each direction of line 
    ray_direction_1 = line[1] - line[0]
    ray_direction_2 = line[0] - line[1]

    # checks if each ray intersects the triangle
    intersect_1 = _calc_ray_triangle_intersect(ray_origin_1, ray_direction_1, triangle)
    intersect_2 = _calc_ray_triangle_intersect(ray_origin_2, ray_direction_2, triangle)
    
    # if intersect found, rounds results to requested decimals
    if intersect_1 is not None:
        intersect_1 = np.round(
            intersect_1,
            decimals=precision,
        )
    if intersect_2 is not None:
        intersect_2 = np.round(
            intersect_2,
            decimals=precision,
        )

    # if both rays intersect, returns the intersection point 
    # otherwise returns None 
    if (
        isinstance(intersect_1, np.ndarray)
        and isinstance(intersect_2, np.ndarray)
        and all(i1 == i2 for i1, i2 in zip(intersect_1, intersect_2))
    ):
        result = intersect_1
    else:
        result = None

    return result


def calc_seg_mesh_intersect(
    datastack, 
    seg_ids, 
    mesh_address, 
    return_intersects=False,
):
    """
    Calculate the point at which the skeletons of a list of segments intersect a mesh, if any.

    By default returns a list of True/False values, optional toggle allows for lists of intersection points.

    Args:
        datastack (str):
            the name of the datastack that contains the segments
            e.g. "brain_and_nerve_cord"
        seg_ids (list of ints):
            the ids fo the segments to check
        mesh_address (str):
            the hosting address of the mesh to check the skeletons against
            e.g. "https://c10s.pni.princeton.edu/tracers/jay/mesher_demo/example_01|neuroglancer-precomputed:"
        return_intersects (bool, optional, default=False):
            optional toggle that will return a list of all the intersection points between 
            the neuron skeletons and the rough area meshes if True, 
            otherwise returns list of True/False values for each neuron 
    """

    # skeletonizes segments using id list and datastack name
    skeletons = get_seg_skeletons(datastack=datastack,seg_ids=seg_ids)

    # creates list of (n,2,3)-shape arrays of endpoint pairs for each edge in each skeleton
    catacombs = [get_bones(datastack=datastack, skeleton=skeleton) for skeleton in skeletons]

    # gets list of triangle point trio arrays from rough spot meshes
    triangles = get_mesh_triangles(volume_path=mesh_address)

    # makes empty list to populate with interseection points
    intersects = []

    # gets all intersection points for each skeleton, adds list to main 'intersects' list
    # this will add None value instead of list if no intersection points are found
    for skeleton in catacombs:
        intersections = calc_skeleton_mesh_intersect(skeleton, triangles)
        intersects.append(intersections)

    # if user requested intersection points, sets return value to intersects list
    # otherwise populates return list with True/False values for each segment
    if return_intersects == True:
        results = intersects
    else:
        results = [i != None for i in intersects]

    return results


def calc_skeleton_mesh_intersect(
    bones, 
    mesh_triangles,
):
    """
    Calculates all the points at which a skeleton intersects a mesh. 
    
    Point coordinates for bones and mesh triangles must be in the same voxel resolution.

    Args:
        bones ((n,2,3)-shape numpy array of floats):
            an array of pairs of point coordinates that define the edges of a skeleton            
        mesh_triangles ((n,3,3)-shape numpy array of floats):
            an array of trios of point coordinates that define the triangles of a mesh 
            

    Returns:
        intersections (list of (3)-shape numpy arrays of floats OR None):
            the intersection points between the skeleton and the mesh if any were found 
            otherwise returns None 
    """

    # makes empty list to populate with intersection points 
    intersections = []

    # checks if each line segment in the skeleton passes through any of 
    # the triangles that make up the mesh and adds intersection points to list
    for line in bones:
        for triangle in mesh_triangles:
            result = calc_line_triangle_intersect(line, triangle)
            if isinstance(result, np.ndarray):
                intersections.append(result)

    # if there were no intersections, sets intersections to None 
    if len(intersections) == 0:
        intersections = None

    return intersections


def check_seg_freshness(
    datastack, 
    seg_ids,
):
    """
    Checks a list of segment IDs to see which are current and which are outdated.

    Args:
    datastack (str):
        the name of the CAVE datastack the seg ids are from
    seg_ids (list of ints):
        a list of segment IDs to check the freshness of

    Returns:
    freshness_list (list of bools):
        a list of True/False values for each segment ID in the list submitted
    """

    # sets client using datastack name
    client = CAVEclient(datastack)

    # creates list by checking the freshness of each seg and converting to bool
    freshness_list = [
        bool(sniff) for sniff in client.chunkedgraph.is_latest_roots(seg_ids)
    ]

    return freshness_list


def check_seg_proofread_status(
    datastack, 
    seg_ids,
):
    """
    Checks if a list of segment IDs are marked as "backbone proofread" or not.

    Args:
        datastack (str):
            the name of the CAVE datastack the segments belong to
        seg_ids (list of ints):
            a list of segment IDs to check

    Returns:
        out_list (list of bools):
            a list of True/False values denoting proofreading status
    """

    # sets config and cave client using datastack name 
    config = get_config(datastack=datastack)
    client = CAVEclient(datastack)

    # gets names of proofreading table and relevant columns from config 
    proofreading_table = config["proofreading_table_name"]

    # handles datastacks without a default proofreading table
    if proofreading_table == None:
        print("Error: The requested datatack doesn't have a proofreading table.")
        return

    # gets column names from config
    seg_col = config["proofreading_table_seg_col"]
    proof_col = config["proofreading_table_status_col"]

    # makes dataframe of all seg_ids that appear in proofreading table 
    df = client.materialize.query_table(
        proofreading_table, 
        filter_in_dict={seg_col: seg_ids},
    )

    # makes empty list to fill with proofreading statuses 
    out_list = []

    # checks if each seg is in the df and if its proofreading status is marked as True 
    # appends result to output list 
    for seg in seg_ids:
        if seg in df[seg_col].values:
            proofs = df.loc[df[seg_col] == seg, proof_col]
            if False not in proofs:
                out_list.append(True)
            else:
                out_list.append(False)
        else:
            out_list.append(False)

    return out_list


def convert_coord_res(
    point_coords, 
    res_current=[1, 1, 1], 
    res_desired=[1, 1, 1],
):
    """
    Converts the coordinates of a 3D point between two resolutions.

    Args:
        point_coords (list of ints):
            point coordinates in current resolution
            e.g. [1,2,3]
        res_current (list of ints, optional, default=[1,1,1]):
            current x,y,z resolution in nm/voxel, 
            e.g. [4, 4, 40]
        res_desired (list of ints, optional, default=[1,1,1]):
            desired x,y,z resolution in nm/voxel, 
            e.g. [16, 16, 40]

    Returns:
        converted_point_coords (list of ints):
            point coordinates after conversion
    """

    # converts coordinates by dividing each by the ratio of desired/current resolution 
    converted_point_coords = [
        int(coord / (res_des / res_cur))
        for coord, res_cur, res_des in zip(point_coords, res_current, res_desired)
    ]

    return converted_point_coords


def count_synapses(
    datastack, 
    seg_ids, 
    detailed_results=False,
):
    """
    Gets synapse counts for a list of segment IDs.

    Arguments:
        datastack (str):
            the name of the CAVE datastack the IDs are from
            e.g. "brain_and_nerve_cord"
        seg_ids (list of ints):
            a list of segment IDs to get synapse counts for
        detailed_results (bool, optional, default=False):
            optional toggle to get dictionary output with incoming and outgoing numbers
            by default only returns total synapse number 

    Returns:
        synapses (list of ints OR dict):
            if detailed_results=False, a list of total synapse counts in the same order as the seg IDs submitted
            if detailed_counts=True, a dictionary with seg IDs as keys and detailed synapse counts as values   
    """

    # ensures seg IDs are ints for feeding into table query
    seg_ids = list(map(int, seg_ids))

    # sets CAVE client object using datastack name
    client = CAVEclient(datastack_name=datastack)

    # gets config info for datastack
    # throws error if incompatible name used
    try:
        config = get_config(datastack=datastack)
    except KeyError:
        raise KeyError(
            "The datastack you requested is not supported. For a list of supported datastacks, use get_datastack_names()."
        )

    # gets name of synapse table using stack_info
    table_name = config["synapse_table_name"]

    # throws error if datastack has no synapse table in config dict
    if table_name == None:
        raise AttributeError(
            "The requested datastack doesn't have a supported synapse table."
        )

    # sets names of columns for pre- and post-synaptic seg ids
    pre_name = config["syn_pre_seg_col"]
    post_name = config["syn_post_seg_col"]

    # makes dfs of incoming and outgoing synapses entries for all seg_ids in list
    in_df = client.materialize.query_table(
        table_name,
        filter_in_dict={post_name: seg_ids},
    )
    out_df = client.materialize.query_table(
        table_name,
        filter_in_dict={pre_name: seg_ids},
    )

    # counts occurrences of each unique value in dfs
    in_counts = in_df[post_name].value_counts()
    out_counts = out_df[pre_name].value_counts()

    # handles 0-synapse segments
    for seg_id in seg_ids:
        if seg_id not in in_counts:
            in_counts[seg_id] = 0
        if seg_id not in out_counts:
            out_counts[seg_id] = 0

    # handles output formatting if detailed results requested
    if detailed_results == True:

        # creates empty synapse dict to fill with counts
        synapses = {}

        # fills synapse dict with count dicts
        for seg_id in seg_ids:
            if len(in_df) == 0:
                incoming = 0
            else:
                incoming = int(in_counts[seg_id])
            if len(out_df) == 0:
                outgoing = 0
            else:
                outgoing = int(out_counts[seg_id])
            synapses[seg_id] = {
                "in": incoming,
                "out": outgoing,
                "all": incoming + outgoing,
            }

    # handles normal list output formatting
    else:
        # makes list of summed incoming and outgoing numbers for each seg_id
        synapses = [int(in_counts[seg_id] + out_counts[seg_id]) for seg_id in seg_ids]

    return synapses    


def count_user_sv_contribution(
    datastack, 
    completed_seg_id,
):
    """
    Counts how many unique supervoxels each user was responsible for adding to or removing from a segment.
    
    Merges only credit the smaller of the two pieces.
    Each user can only get credit for each supervoxel once,
    but one supervoxel may be credited to multiple users.
    May take several minutes to run for large neurons.
    Intended for use at the time a user marks the cell "backbone proofread".

    Args:
        datastack (str):
            the name of the CAVE datastack the segment is in
            e.g. "brain_and_nerve_cord"
        completed_seg_id (int):
            the segment ID of the completed cell

    Returns:
        counts (dict):
            dictionary of user IDs with supervoxel counts
    """

    # sets client using datastack name
    client = CAVEclient(datastack_name=datastack)

    # makes df of changelog for requested seg
    df = client.chunkedgraph.get_tabular_change_log(root_ids=[completed_seg_id])[
        completed_seg_id
    ]

    # gets list of all supervoxel IDs in final segment
    final_svs = set(client.chunkedgraph.get_leaves(completed_seg_id))

    # gets list of all users who worked on neuron
    users = df["user_id"].unique().tolist()

    # makes dict of users with empty supervoxel sets
    user_svs = {user: set() for user in users}

    # iterates over edits and add relevant supervoxel IDs to each user's set in user_svs
    # tqdm adds progress bar print so you can estimate time for large neurons
    for r in tqdm(df.itertuples(index=False), total=df.shape[0]):
        # get user id for edit
        u = r.user_id

        # if edit is split, adds svs from pre-split segment that didn't make it into final segment
        if r.is_merge == False:
            before_seg = r.before_root_ids[0]
            after_seg = r.after_root_ids[0]
            before_svs = set(client.chunkedgraph.get_leaves(before_seg))
            after_svs = set(client.chunkedgraph.get_leaves(after_seg))
            keep_svs = {
                sv for sv in before_svs if sv not in after_svs and sv not in final_svs
            }

        # if edit is merge, adds svs from smaller pre-split segment that made it into final segment
        elif r.is_merge == True:
            a = r.before_root_ids[0]
            b = r.before_root_ids[1]
            a_svs = set(client.chunkedgraph.get_leaves(a))
            b_svs = set(client.chunkedgraph.get_leaves(b))
            if len(a_svs) > len(b_svs):
                keep_svs = {sv for sv in b_svs if sv in final_svs}
            else:
                keep_svs = {sv for sv in a_svs if sv in final_svs}

        # adds relevant supervoxels to user's dict entry
        user_svs[u].update(keep_svs)

    # counts up all supervoxels assigned to each user and make df of results
    counts = {user: len(user_svs[user]) for user in users}

    return counts

# def fix_mesh_error(
#     datastack, 
#     seg_id, 
#     bbox,
# ):
#     """
#     Tries to fix a mesh issue by remeshing a specific chunk of a specific neuron.

#     WARNING: THIS FUNCTION IS CURRENTLY BROKEN

#     Args:
#         datastack (str):
#             name of CAVE datastack you're working with as a string
#             e.g. "brain_and_nerve_cord"
#         seg_id (int)
#             segment id of the neuron you want to remesh
#         bbox (list of lists of ints):
#             xyz coords of bounding box annotation corners for the region of space you want to remesh
#             e.g. [[x1,y1,z1],[x2,y2,z2]]
#     """

#     # gets config dict
#     config = get_config(datastack=datastack)

#     # sets resolution using config
#     res = config["resolution"]

#     # converts bbox corner point coords to nanometer resolution
#     bbox = [tt.convert_coord_res(bound,res_current=res) for bound in bbox]

#     # converts bbox coords into correct format for get_leaves method
#     bbox_bounds = np.array([sorted([c1, c2]) for c1, c2 in zip(bbox[0], bbox[1])])

#     # sets cave client
#     client = CAVEclient(datastack)

#     # gets L2 node IDs
#     L2_ids = client.chunkedgraph.get_leaves(
#         root_id=seg_id, 
#         bounds=bbox_bounds, 
#         stop_layer=2
#     )

#     # remeshes the selected neuron in the selected region
#     client.chunkedgraph.remesh_level2_chunks(chunk_ids=L2_ids)


def get_anno_array_from_json_state_file(
    layer_name, 
    json_filepath,
):
    """
    Extracts a numpy array of point coords from a point annotation layer in a NG JSON state file. 

    Args:
        layer_name (str):
            the name of the annotation layer to pull coordinates from
            e.g. "annotation1"
        json_filepath (str):
            the absolute filepath to the NG state json file to pull annotations from
            e.g. '/home/username/ng_jsons/state.json'

    Returns:
        points ((n,3)-shape numpy array of ints):
            numpy array of annotation point coordinates
    """

    # opens json file and converts to python dict 
    with open(json_filepath, "r") as json_file:
        json_dict = json.load(json_file)

    # searches the full dict for the annotation layer specified and pulls it out as a separate list
    for layer in json_dict["layers"]:
        if layer["name"] == layer_name:
            anno_raw_list = layer["annotations"]

    # creates an empty list to fill with points
    points = []

    # pulls the actual coordinate info out of the layer list
    for anno in anno_raw_list:
        points.append(anno["point"])

    # converts points list to numpy array
    points = np.array(points)

    return points


def get_bones(
    datastack, 
    skeleton,
):
    """
    Gets an array of viewer-resolution endpoint pairs for each edge in a nm-res osteoid skeleton.

    Args:
        datastack (str):
            the name of the CAVE datastack the skeleton is from 
            e.g. 'brain_and_nerve_cord'
        skeleton
            the osteoid-format skeleton object in nanometer [1,1,1] voxel resolution

    Returns:
        bones ((n,2,3)-shape numpy array)
            array of endpoint pairs for each edge of the skeleton in volume resolution
    """

    # gets bone endpoints from the vertex list using indices from edge list 
    nm_bones = np.array(
        [
            [skeleton.vertices[edge[0]], skeleton.vertices[edge[1]]]
            for edge in skeleton.edges
        ]
    )

    # gets config dict for datastack 
    config = get_config(datastack=datastack)

    # gets voxel resolution from config dict 
    res = config["resolution"]

    # creates empty list to populate with volume-resolution bones 
    bones = []

    # converts bones from nm to volume resolution 
    for nm_bone in nm_bones:
        bone = []
        for nm_point in nm_bone:
            point = [x / y for x, y in zip(nm_point, res)]
            bone.append(point)
        bones.append(bone)

    # converts bones list to numpy array of floats as it returns 
    return np.array(bones, dtype=float)


def get_cable_lengths(
    datastack, 
    seg_ids,
):
    """
    Gets a list of cable lengths for the skeletons of submitted root ids.

    Args:
        datastack (str):
            the name of the CAVE datastack the segments are from
            e.g. "brain_and_nerve_cord"
        seg_ids (list of ints):
            a list of segment IDs to get synapse counts for

    Returns:
        cable_lengths (list of floats):
            a list of cable lengths for each segment
    """

    # gets osteoid skeletons for each seg
    graveyard = get_seg_skeletons(datastack=datastack,seg_ids=seg_ids)

    # makes list of cable lengths for each skeleton
    cable_lengths = [float(skeleton.cable_length()) for skeleton in graveyard]

    return cable_lengths


def get_cave_stacks():
    """
    Gets a list of all the currently-documented CAVE datastack names.

    Returns:
        stacks (list of str):
            a list of all the current datastack names
    """

    # sets generic cave client
    client = CAVEclient()

    # pulls list of all currently-documented datastacks
    stacks = client.info.get_datastacks()

    return client.info.get_datastacks()


def get_cave_stack_info(datastack):
    """
    Gets the metadata information for a specific CAVE datastack.

    Args:
        datastack (str):
            the name of the datastack you want information for
            e.g. "brain_and_nerve_cord"

    Returns:
        stack_info (dict):
            a dictionary containing the official published metadata info for the requested datastack
    """

    # sets cave client using datstack name
    client = CAVEclient(datastack)

    # gets metadata for requested stack
    stack_info = client.info.get_datastack_info()

    return stack_info


def get_cave_stack_tables(datastack):
    """
    Gets all the currently-listed tables for a specific CAVE datastack.

    Argument:
        datastack (str):
            the name of the datastack you want information for
            e.g. "brain_and_nerve_cord"

    Returns:
        stack_tables (list of str):
            names of all currently-documented tables for the requested datastack
    """

    # sets client using datastack name 
    client = CAVEclient(datastack_name=datastack)

    # pulls datastact info dictionary using stack name
    stack_tables = client.annotation.get_tables()

    return stack_tables

def get_cave_table(
    datastack, 
    table_name,
):
    """
    Get the data as a pandas dataframe for a specific table in a specific CAVE datastack.

    Some tables may have limits on the number of rows you can pull at once.

    Args:
        datastack (str):
            the name of the CAVE datastack you want information for
            e.g. "brain_and_nerve_cord"
        table_name (str):
            the name of the table to request data for
            e.g. "cell_ids"

    Returns:
        table_df (Pandas DataFrame object):
            the data for the requested table
    """

    # sets client using datastack name
    client = CAVEclient(datastack_name=datastack)

    # pulls datastact info dictionary using stack name
    table_df = client.materialize.query_table(table_name)

    return table_df


def get_cave_table_info(
    datastack, 
    table_name,
):
    """
    Gets the metadata for a specific table in a specific CAVE datastack.

    Args:
        datastack (str):
            the name of the CAVE datastack you want information for
            e.g. "brain_and_nerve_cord"
        table_name (str):
            the name of the table to request metadata for
            e.g. "cell_ids"
        
    Returns:
        table_data (dict):
            all the metadata on the requested table
    """

    # sets client using datastack name 
    client = CAVEclient(datastack_name=datastack)

    # pulls datastact info dictionary using stack name 
    table_data = client.materialize.get_table_metadata(table_name)

    return table_data


def get_config(datastack):
    """
    Gets the in-house tracer-format config dictionary for a given dataset. 
    
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
            "here_be_monsters": "nokura://tracers/triage_meshes/banc/image",
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
            "here_be_monsters": None,
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
            "here_be_monsters": None,
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
            "here_be_monsters": None,
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
        #     "here_be_monsters" : "",
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


def get_current_seg_id(
    datastack, 
    seg_id, 
    include_ratio=False, 
    full_list=False, 
    skip_fresh=True
):
    """
    Gets the most likely candidate for the current version of a stale segment id.

    DEPRECATION WARNING: When use repeatedly in a short time, this function can get throttled by CAVE 
    due to an inefficiency in setting the client. It will eventually be merged with update_seg_list() 
    to become get_current_seg_ids().

    Args:
        datastack (str):
            the name of the CAVE datastack the segment id is from
            e.g. "brain_and_nerve_cord"
        seg_id (int):
            the potentially-outdated ID of the segment you want the current ID for
        include_ratio (bool, optional, default=False):
            if True will include proportion of stale segment's supervoxels that
            are contained within fresh rosegmentot
        full_list (bool, optional, default=False):
            if True will return a list of all the fresh IDs associated with 
            supervoxels from the "stale" ID instead of just the top candidate
        skip_fresh (bool, optional, default=True):
            if False, skips checking if the ID is already current, 
            main usage is a slight performance increase on a long list of 
            IDs known to all be outdated

    Returns:
        result (varies):
            output depends on input toggles
            by default returns the integer segment id of the most likely current segment
            if include_ratio is True, retruns a 2-item list [seg_id, ratio]
            if full_list is true, returns list of all associate seg_ids as ints
            if both include_ratio and full_list are True, returns list of 2-item lists [seg_id, ratio]
    """

    # prints deprecation warning
    print("DEPRECATION WARNING: When use repeatedly in a short time, this function can get throttled by CAVE") 
    print("due to an inefficiency in setting the client. It will eventually be merged with update_seg_list()") 
    print("to become get_current_seg_ids().")

    # checks if seg_id is already fresh, returns if so
    if skip_fresh == True and check_seg_freshness(datastack, [seg_id])[0] == True:
        return seg_id

    # sets client using datastack
    client = CAVEclient(datastack)

    # gets a list of all the supervoxels associated with a stale id
    svs = client.chunkedgraph.get_leaves(seg_id)

    # gets total number of supevoxels in stale id
    total_sv = len(svs)

    # makes list of the fresh seg id for each supervoxel
    # returns "ERROR" value if neuron is too large
    seg_ids = list(client.chunkedgraph.get_roots(svs))

    # gets unique fresh seg ids from list
    usegs = list(set(seg_ids))

    # makes dict of how many original supervoxels fresh ids contain
    sv_counts = {str(useg): seg_ids.count(useg) for useg in usegs}

    # gets fraction of stale seg supervoxels in each fresh seg
    sv_fracs = [[int(useg), (sv_counts[str(useg)] / total_sv)] for useg in usegs]

    # sorts segs by fraction of original supervoxels
    sv_fracs.sort(key=lambda x: x[1], reverse=True)

    # handles confidence ratio request conditions
    if include_ratio == True:
        result = sv_fracs
    else:
        result = [frac[0] for frac in sv_fracs]

    # handles full list request conditions
    if full_list == True:
        return result
    else:
        return result[0]




def get_current_seg_ids(
    datastack, 
    seg_ids, 
    include_ratio=False, 
    full_list=False, 
    skip_fresh=True,
    detailed_errors=False,
):
    """
    Gets the most likely candidate for the current version of a stale segment id.

    BANDWIDTH WARNING: When looped repeatedly in a short time, as might happen
    when using this to update a spreadsheet one line at a time, this function can get 
    throttled by CAVE due to repeatedly setting the client. Workarounds linclude batching,
    parallelization, or simply setting a sleep delay to lower the request rate below 60/min
    Extremely large neurons may exceed the request limit for the supervoxel query and cause
    an HTTP 413 Client Error.

    Args:
        datastack (str):
            the name of the CAVE datastack the segment id is from
            e.g. "brain_and_nerve_cord"
        seg_id (int):
            the potentially-outdated ID of the segment you want the current ID for
        include_ratio (bool, optional, default=False):
            if True will include proportion of stale segment's supervoxels that
            are contained within fresh rosegmentot
        full_list (bool, optional, default=False):
            if True will return a list of all the fresh IDs associated with 
            supervoxels from the "stale" ID instead of just the top candidate
        skip_fresh (bool, optional, default=True):
            if False, skips checking if the ID is already current, 
            main usage is a slight performance increase on a long list of 
            IDs known to all be outdated
        detailed_errors (bool, optional, default=False):
            normally returns "ERROR" if error is encountered, if this setting is True
            will return a detailed error message for troubleshooting

    Returns:
        result (varies):
            output depends on input toggles
            by default returns the integer segment id of the most likely current segment
            if include_ratio is True, retruns a 2-item list [seg_id, ratio]
            if full_list is true, returns list of all associate seg_ids as ints
            if both include_ratio and full_list are True, returns list of 2-item lists [seg_id, ratio]
    """

    # sets client using datastack
    client = CAVEclient(datastack)

    # make df with columns for stale segs and T/F result of freshness checker
    df = pd.DataFrame(
        {"stale_seg": seg_ids, "already_fresh": check_seg_freshness(datastack, seg_ids)}
    )

    # make empty list to fill with current seg ids #
    fresh_segs = []

    # if seg is already fresh, add to list, otherwise use freshener
    for seg_id in tqdm(seg_ids, total=len(seg_ids),desc="Calculating candidate scores"):
    # for seg_id in seg_ids:
        try:
            if df.loc[df["stale_seg"] == seg_id, "already_fresh"].values[0] == True:
                fresh_seg = [seg_id]
                
                # adds ratio of 1.0 to maintain formatting if ratios requested
                if include_ratio == True:
                    fresh_seg.append(1.0)
                
                # makes nested list to maintain formatting if full list requested
                if full_list == True:
                    fresh_seg = [fresh_seg]

                fresh_segs.append(fresh_seg)
            else:
        
                # gets a list of all the supervoxels associated with a stale id
                svs = client.chunkedgraph.get_leaves(seg_id)

                # gets total number of supevoxels in stale id
                total_sv = len(svs)

                # makes list of the fresh seg id for each supervoxel
                # returns "ERROR" value if neuron is too large
                seg_ids = list(client.chunkedgraph.get_roots(svs))

                # gets unique fresh seg ids from list
                usegs = list(set(seg_ids))

                # makes dict of how many original supervoxels fresh ids contain
                sv_counts = {str(useg): seg_ids.count(useg) for useg in usegs}

                # gets fraction of stale seg supervoxels in each fresh seg
                sv_fracs = [[int(useg), (sv_counts[str(useg)] / total_sv)] for useg in usegs]

                # sorts segs by fraction of original supervoxels
                sv_fracs.sort(key=lambda x: x[1], reverse=True)

                # handles confidence ratio request conditions
                if include_ratio == True:
                    result = sv_fracs
                else:
                    result = [frac[0] for frac in sv_fracs]

                # handles full list request conditions
                if full_list == True:
                    fresh_segs.append(result)
                else:
                    fresh_segs.append(result[0])
        except HTTPError as h:
            if detailed_errors == True:
                fresh_segs.append(f"{h}")
            else:
                fresh_segs.append("ERROR")
        except Exception as e:
            if detailed_errors == True:
                fresh_segs.append(f"{e}")
            else:
                fresh_segs.append("ERROR")

    return fresh_segs


def update_seg_list(datastack, seg_ids):
    """
    Gets the most current seg IDs for a list of seg IDs that may be outdated.

    DEPRECATION WARNING: This function can get throttled by CAVE due to an inefficiency.
    It will eventually be merged with get_current_seg_id() to become get_current_seg_ids().

    Args:
        datastack (str):
            the name of the datastack the segment ids are from
        seg_ids (list of ints):
            a list of segment ids you want to update

    Returns:
        fresh_segs (list of ints):
            a list of current seg ids
    """

    # prints deprecation warning
    print("DEPRECATION WARNING: This function can get throttled by CAVE due to an inefficiency.") 
    print("It will eventually be merged with get_current_seg_id() to become get_current_seg_ids().")

    # make df with columns for stale segs and T/F result of freshness checker
    df = pd.DataFrame(
        {"stale_seg": seg_ids, "already_fresh": check_seg_freshness(datastack, seg_ids)}
    )

    # make empty list to fill with current seg ids #
    fresh_segs = []

    # if seg is already fresh, add to list, otherwise use freshener
    for seg_id in seg_ids:
        if df.loc[df["stale_seg"] == seg_id, "already_fresh"].values[0] == True:
            fresh_segs.append(seg_id)
        else:
            fresh_segs.append(get_current_seg_id(datastack=datastack, seg_id=seg_id))

    return fresh_segs








def get_mesh_triangles(
    volume_path, 
    mesh_seg_id=1, 
    local=False,
):
    """
    Gets an array of the vertices for each face of a neuroglancer precomputed mesh.

    Args:
        volume_path
            the absolute filepath to the directory of the volume that contains the mesh 
            e.g. '/home/username/ng_meshes/image' (str)
        mesh_seg_id (int, optional, default=1):
            the segment ID of the mesh within the neuroglancer volume
        local (bool, optional, default=False):
            if set to True, treats volume path as local file path
            assumes remote-hosted url by default

    Returns:
        triangles ((n,3,3)-shape numpy array of floats):
            the point coordinates of the face vertices for each triangle
            e.g. [[[1,2,3],[4,5,6],[7,8,9]],[[11,12,13],[14,15,16],[17,18,19]],...]
    """

    # removes trailing slashes from volume filepath if present
    if volume_path[-1] == "/":
        volume_path = volume_path[:-1]

    # creates cloudpath using volume path 
    if local == True:
        cloudpath = "file://" + volume_path
    else:
        cloudpath = volume_path

    # creates a cloudvolume object using mesh_path
    try:
        volume = cloudvolume.CloudVolume(cloudpath)
    except FileNotFoundError:
        print(
            f"The directory '{cloudpath}' couldn't be found. Please check the accuracy of this filepath."
        )
    except Exception as e:
        print(f"An error occurred: {e}")

    # pulls the mesh data from the cloudvolume object 
    mesh = volume.mesh.get(mesh_seg_id)

    # gets volume resolution 
    res = volume.resolution

    # pulls the vertex and face data from the mesh 
    verts = mesh.vertices
    faces = mesh.faces

    # creates an empty list to populate with triangle coordinates 
    triangles = []

    # gets point trios for each face and converts nm coords to volume resolution 
    for face in faces:
        triangle = []
        for vindex in face:
            point = [x / y for x, y in zip(verts[vindex], res)]
            triangle.append(point)
        triangles.append(triangle)

    # converts triangle list to numpy array 
    triangles = np.array(triangles)

    return triangles


def get_original_seg_ids(
    datastack, 
    seg_id,
):
    """
    Gets list of IDs for original segments that have since been absorbed by the requested segment.

    Args:
        datastack (str):
            the name of the CAVE datastack the IDs are from
            e.g. "brain_and_nerve_cord"
        seg_id (int)
            the ID of the segment you want the origina segment IDs for

    Returns:
        seg_ids (list of ints):
            a list of IDs of the original segments that were wholly or partially absorbed 
            by the requested segment during the course of its proofreading
    """

    # sets cave client using datastack
    client = CAVEclient(datastack)

    # pulls seg list and converts array of numpy int64s to list of ints 
    seg_ids = [int(seg) for seg in client.chunkedgraph.get_original_roots(seg_id)]

    return seg_ids


def get_roots_from_points(
    datastack,
    points,
    sv=False,
):
    """
    Get IDs for the segment or supervoxel at a list of point coordinates.

    Args:
        datastack (str):
            the name of the CAVE datastack the coords are in
            e.g. "brain_and_nerve_cord"
        points (list of lists of ints):
            a list of point coordinates you want the root ID for
            e.g. [[1,2,3],[4,5,6],...]
        sv (bool, optional, default=False):
            if True, returns supervoxel IDs, otherwise returns segment IDs

    Returns:
        root_ids (list of ints): 
            the IDs of the segments or supervoxels at the locations requested
    """

    # allows for single-dimension list input for one set of coords
    if type(points[0]) == int:
        points = [points]

    # creates empty list to populate with root IDs
    root_ids = []

    # sets client
    client = CAVEclient(datastack_name=datastack)

    # gets datastack config
    config = get_config(datastack=datastack)

    # gets segmentation address
    seg_url = config["seg_source_url"]

    # sets cloud volume
    volume = cloudvolume.CloudVolume(
        seg_url,
        use_https=True,
    )

    # gets mip0 resolution
    mip0_res = volume.meta.resolution(0)

    # gets viewer resolution
    viewer_res = config["resolution"]

    # creates a conversion template for going from viewer to mip0 coords
    res_conversion = [mip0 / viewer for mip0, viewer in zip(mip0_res, viewer_res)]

    # gets requested root for each coordinate in list of coords
    for point in points:
        try:
            # converts the viewer coords to mip0
            fixed_point = [xyz / res for xyz, res in zip(point, res_conversion)]

            # creates a cloudvolume.Bbox object to feed into the downloader
            bbox = cloudvolume.Bbox(fixed_point, [coord + 1 for coord in fixed_point])

            # downloads a list of all the supervoxel IDs inside the bounding box
            vol_dl = volume.download(
                bbox=bbox,
            )

            # pulls the svid out of the nested series of lists that exist for larger bboxes
            sv_id = vol_dl[0][0][0][0]

            # handles return format choice
            if sv == True:
                # if supervoxel ID requested, add to output list
                root_ids.append(sv_id)
            else:
                # if segment requested, get seg ID using sv ID and add to output list
                root_ids.append(client.chunkedgraph.get_root_id(supervoxel_id=sv_id))
        # adds "ERROR" value if something goes wrong so as not to let one failure break long list
        except:
            root_ids.append("ERROR")

    return root_ids


def get_seg_3d_volume(
    datastack,
    seg_id,
):
    """
    Gets the volume of a given segment in cubic micrometers.

    Args:
        datastack (str):
            the name of the CAVE datastack the segment ID belongs to
            e.g. "brain_and_nerve_cord"
        seg_id (int)
            the ID of the segment you want the 3D volume for

    Returns:
        vol (float):
            the volume of the segment requested in cubic micrometers
    """

    # sets CAVE client using datastack name 
    client = CAVEclient(datastack_name=datastack)

    # gets all the L2-level info about the seg ID submitted 
    l2nodes = client.chunkedgraph.get_leaves(seg_id, stop_layer=2)

    # pulls the volume data for all the l2nodes 
    l2stats = client.l2cache.get_l2data(l2nodes, attributes=["size_nm3"])

    # converts the l2stats into a dataframe 
    l2df = pd.DataFrame(l2stats).T

    # calculates the volume of the neuron by summing the nm3 volumes of 
    # its constituent L2 nodes and dividing into um3 
    vol = l2df.size_nm3.sum() / (1000 * 1000 * 1000)

    return vol


def get_seg_changelog(
    datastack, 
    seg_id,
):
    """
    Gets the tabular changelog for a given segment as a dataframe.

    Args:
        datastack (str):
            the name of the CAVE datastack the seg id is from
            e.g. "brain_and_nerve_cord"
        seg_id (int):
            the segment id you want the changelog for

    Returns:
        df (pandas DataFrame object):
            a dataframe of all the changelog information
    """

    # sets client using datastack name
    client = CAVEclient(datastack)

    # gets one-item dict of changelog
    log = client.chunkedgraph.get_tabular_change_log([seg_id])

    # pulls df from dict using seg id as key
    df = log[seg_id]

    return df


def get_seg_details(
    datastack, 
    seg_ids,
):
    """
    Gets current seg ID, 3D volume in um3, cable length, and synapse count for a list of seg IDs.

    Args:
        datastack (str):
            the name of the CAVE datastack the IDs are from
            e.g. "brain_and_nerve_cord"
        seg_ids (list of ints):
            a list of segment IDs to get details for

    Returns:
        out_rows (list of lists):
            a list of lists, for ehich each entry will be structured as
            [original ID, current id, volume, cable length, ougoing syns, incoming sysns, total syns]
    """

    # gets current ids for each seg
    fresh_segs = [
        str(get_current_seg_id(datastack=datastack, seg_id=seg_id)) for seg_id in seg_ids
    ]

    # makes list of segment volumes using fresh segs
    vols = [float(get_seg_3d_volume(datastack=datastack,seg_id=fresh_seg)) for fresh_seg in fresh_segs]

    # makes list of cable lengths using fresh segs
    cable_lengths = get_cable_lengths(
        datastack=datastack,
        seg_ids=fresh_segs,
    )

    # gets detailed synapse data for each fresh seg
    synapses = count_synapses(
        datastack=datastack,
        seg_ids=fresh_segs,
        detailed_results=True,
    )

    # formats all the information into a list of spreadsheet-stlye rows
    # the reason for this formatting is primarily for ease of use with gsheet tools
    out_rows = [
        [
            seg_id,
            fresh_seg,
            vol,
            cable,
            synapses[int(fresh_seg)]["out"],
            synapses[int(fresh_seg)]["in"],
            synapses[int(fresh_seg)]["all"],
        ]
        for seg_id, fresh_seg, vol, cable in zip(seg_ids, fresh_segs, vols, cable_lengths)
    ]

    return out_rows


def get_seg_edits(
    datastack, 
    seg_id, 
    op_column="operation_id",
):
    """
    Gets a dataframe of all the changes made to a single segment id.

    For split operations, multiple pairs of point coordinates exist on the backend. 
    This function averages them into a single pair for ease of use.

    Args:
        datastack (str):
            the name of the CAVE datastack the segment ID is from
                e.g. "brain_and_nerve_cord"
        seg_id (int):
            a segment ID to get the edit history for
        op_column (str, optional, default="operation_id"):
            the name of the column in the changelog that holds the operation ids for each edit 
            
    Returns:
        final_df (pandas DataFrame object):
            a dataframe containing relevant information for each edit made to a segment 
    """

    # sets client using datastack name
    client = CAVEclient(datastack)

    # makes df of changelog for neuron
    cl_df = get_seg_changelog(datastack=datastack, seg_id=seg_id)

    # makes output df from operation id column of changelog df
    final_df = cl_df[["operation_id"]].copy()
    final_df.reset_index(drop=True, inplace=True)

    # gets dict of operation details
    op_ids = cl_df["operation_id"].values.tolist()
    opdeet_dict = client.chunkedgraph.get_operation_details(operation_ids=op_ids)

    # creates empty lists to populate with data
    seg_pairs = []
    before_ids = []
    after_ids = []
    is_merge = []
    users = []
    point_coords = []

    # pulls relevant data from changelog df and operation dict
    # adds to relevant lists
    for op_id in op_ids:

        # gets details for this operation from main dictionary
        op = opdeet_dict[str(op_id)]

        # gets user id for this operation from changelog dataframe
        users.append(cl_df.loc[cl_df["operation_id"] == op_id, "user_id"].iloc[0])

        # gets id(s) of pre-operation seg(s)
        before = cl_df.loc[cl_df["operation_id"] == op_id, "before_root_ids"].iloc[0]
        before_ids.append(before)

        # detects merge operations
        if len(before) == 2:
            # sets relevant seg pair to pre-opertaion segs for merges
            seg_pair = before

            # adds post-operation id from changelog dataframe
            after_ids.append(
                cl_df.loc[cl_df["operation_id"] == op_id, "after_root_ids"].iloc[0]
            )

            # sets is_merge to True, denoting a merge operation
            is_merge.append(True)

            # gets operation coordinates for line anntoations
            point_coords.append([op["source_coords"][0], op["sink_coords"][0]])

        # detects split operations
        else:
            # sets relevant seg pair to post-opertaion segs for splits
            # pulls from operation detail dict for splits instead of changleog df
            seg_pair = opdeet_dict[str(op_id)]["roots"]

            # adds post-operation ids
            after_ids.append(seg_pair)

            # sets is_merge to False, denoting a split operation
            is_merge.append(False)

            # gets operation coordinates for line anntoations
            # for splits, multiple coords are given, so must be averaged
            point_coords.append(
                [
                    calc_avg_point_coords(points=op["source_coords"]),
                    calc_avg_point_coords(points=op["sink_coords"]),
                ]
            )

            # unused code for implementing option to see all coords for split
            # coord_cluster = [[source_coord,sink_coord] for source_coord,sink_coord in zip(op["source_coords"],op["sink_coords"])]

        # adds chosen seg pair to list
        seg_pairs.append(seg_pair)

    # adds data lists to final df as columns
    final_df["is_merge"] = is_merge
    final_df["point_coords"] = point_coords
    final_df["before_segs"] = before_ids
    final_df["after_segs"] = after_ids
    final_df["seg_pairs"] = seg_pairs
    final_df["user"] = users

    return final_df


def get_seg_from_sv(
    datastack, 
    sv_id,
):
    """
    Gets segment ID using supervoxel ID and dataset.

    Args:
        datastack (str):
            the name of the CAVE datastack the supervoxel is in
        sv_id (int):
            the ID of the supervoxel
        
    Returns:
        seg_id (int):
            the segment ID that supervoxel currently belongs to
    """

    # sets client using datastack name
    client = CAVEclient(datastack)

    # looks up seg ID using supervoxel ID
    seg_id = client.chunkedgraph.get_root_id(supervoxel_id=sv_id)

    return seg_id


def get_seg_skeletons(
    datastack, 
    seg_ids,
):
    """
    Gets a list of osteoid-format skeletons for a list of segment IDs.

    Arguments:
        datastack (str):
            the name of the CAVE datastack the segment IDs belong to 
            for a list of currently-supported datastacks, use the get_supported_configs() function
        seg_ids (list of ints):
            a list of the segment IDs you want skeletons for

    Returns:
        intersect_list (list of objects):
            a list of osteoid skeleton objects in the same ordaer as the submitted segment IDs
    """

    # sets client using datastack_name 
    client = CAVEclient(datastack)

    # pulls tracer-format datastack config 
    config = get_config(datastack=datastack)

    # gets datastack esolution from config 
    stack_res = config["resolution"]

    # creates matrix using datastack resolution for converting skeleton coords from nm res 
    matrix = np.array(
        [
            [stack_res[0], 0, 0, 0],
            [0, stack_res[1], 0, 0],
            [0, 0, stack_res[2], 0],
        ],
        dtype=np.float32,
    )

    # tells cave server to generate skeletons for all IDs in list 
    # returns time estimate in seconds 
    seconds = client.skeleton.generate_bulk_skeletons_async(
        seg_ids, skeleton_version=-1
    )

    # checks if seconds is a dictionary, throws bad seg ID error and quits if so 
    # unclear why? 
    if isinstance(seconds, dict):
        print("Bad segment id.")
        sys.exit(0)

    # prints the time estimate for the user 
    print(f"Skeletonization ETA {seconds} seconds.")

    # sleeps for the estimated amount of time 
    time.sleep(seconds)

    # gets the now-generated skeletons from the cave server and makes them into a list 
    cave_skeletons = [client.skeleton.get_skeleton(seg_id) for seg_id in seg_ids]

    # for each cave skeleton in the list, converts to osteoid skeleton using Skeleton() 
    # transforms nanometer coords to volume resolution using matrix 
    osteoid_skeletons = [
        Skeleton(
            vertices=skeleton["vertices"],
            edges=skeleton["edges"],
            radii=skeleton["radius"],
            transform=matrix,
            space="physical",
        )
        for skeleton in cave_skeletons
    ]

    return osteoid_skeletons


def get_state_json_from_url(
    datastack, 
    share_url,
):
    """
    Derives state JSON from shortened sharing url.

    Args:
        datastack (str):
            the name of the CAVE datastack the link is for
            e.g. brain_and_nerve_cord
        share_url (str):
            the shortened NG url you want the JSON for

    Returns:
        state_json (dict):
            the state JSON of the shortened link as a dictionary
    """

    # sets client using datastack name
    client = CAVEclient(datastack)

    # splits share url into components between slashes
    split_url = share_url.split("/")

    # gets state ID, which is always last component
    state_id = int(split_url[-1])

    # retreives JSON from state server using state ID
    state_json = client.state.get_state_json(state_id)

    return state_json


def get_svs_from_seg(
    datastack, 
    seg_id,
):
    """
    Gets IDs of all supervoxels that make up a given segment.

    Args:
        datastack (str):
            the name of the CAVE datastack the segment belongs to
            e.g. "brain_and_nerve_cord"
        seg_id (int):
            the ID of the segment you want supervoxels for
        
    Returns:
        sv_ids (list of ints):
            a list of all the supervoxel IDs that currently belong to the segment
    """

    # sets client using datastack name
    client = CAVEclient(datastack)

    # gets supervoxel IDs using seg ID
    sv_ids = list(client.chunkedgraph.get_leaves(seg_id))

    return sv_ids


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


def gsheet_add_column(
    sheet_key,
    tab_name,
    col_data,
):
    """
    Adds a list as a column to a tab in a google sheet.

    This will fill the first empty column in the chosen tab.
    This function requires a Google authentication token to be set up prior to use.
    The process for doing so is explained here: https://docs.gspread.org/en/latest/oauth2.html#oauth-client-id

    Args:
        sheet_key (str):
            the key for the google sheet
            can be found in the url of the sheet between '/d/' and '/edit?'
        tab_name (str):
            the name of the tab you want to update within the google sheet
            "tab" is an informal term, officially these are called "worksheets" within Google's documentation
        col_data (list):
            a list of values that you want to append as a column to the end of the current data in the sheet
            be aware that large integers passed may sometimes be converted to scientific notation
            it's recommended to pass all data to the spreadsheet as strings if possible to avoid this
    """

    # sets up google credentials
    gc = gspread.oauth()

    # opens sheet as object using sheet key
    sheet = gc.open_by_key(sheet_key)

    # sets the tab you want to update using tab name
    tab = sheet.worksheet(tab_name)

    # gets number of first empty column
    col = len(tab.row_values(1)) + 1

    # adds column data to sheet
    tab.insert_cols(values=[col_data], col=col)


def gsheet_add_row(sheet_key, tab_name, row_data):
    """
    Adds a list as a row to a tab in a google sheet.

    This will fill the first empty row in the chosen tab.
    This function requires a Google authentication token to be set up prior to use.
    The process for doing so is explained here: https://docs.gspread.org/en/latest/oauth2.html#oauth-client-id

    Args:
        sheet_key (str):
            the key for the google sheet
            can be found in the url of the sheet between '/d/' and '/edit?'
        tab_name (str):
            the name of the tab you want to update within the google sheet
            "tab" is an informal term, officially these are called "worksheets" within Google's documentation
        row_data (list):
            a list of values that you want to append as a row to the end of the current data in the sheet
            be aware that large integers passed may sometimes be converted to scientific notation
            it's recommended to pass all data to the spreadsheet as strings if possible to avoid this
    """

    # sets up google credentials
    gc = gspread.oauth()

    # opens sheet as object using sheet key
    sheet = gc.open_by_key(sheet_key)

    # sets the tab you want to update using tab name
    tab = sheet.worksheet(tab_name)

    # adds your row data at the end of any existing data
    tab.append_row(row_data)


def gsheet_add_seg_details(
    datastack,
    sheet_key,
    tab_name,
    volume=True,
    cable_length=True,
    synapse_counts=True,
    proofreading=True,
):
    """
    Gets neuron details for a list of segment IDs in a google sheet and add them to the sheet.
    
    Requires a tab in the sheet with a single column of segment IDs with a header.
    This function requires a Google authentication token to be set up prior to use.
    The process for doing so is explained here: https://docs.gspread.org/en/latest/oauth2.html#oauth-client-id

    Args:
        datastack (str):
            the name of the CAVE datastack the IDs belong to
            e.g. "brain_and_nerve_cord"
        sheet_key (str):
            the key for the google sheet to be updated, found in the url between '/d/' and '/edit?'
        tab_name (str):
            the name of the google sheet tab the list of IDs are in
            "tab" is an informal term, officially these are called "worksheets" within Google's documentation
        volume (bool, optional, default=True):
            whether or not to include 3D volume data in um3
        cable_length (bool, optional, default=True):
            whether or not to include skeleton cable length data
        synapse_counts (bool, optional, default=True):
            whether or not to include synapse data
        proofreading (bool, optional, default=True):
            whether or not to proofreading status
    """

    # sets up google credentials
    gc = gspread.oauth()

    # opens sheet as object using sheet key
    sheet = gc.open_by_key(sheet_key)

    # sets the tab you want to update using tab name
    tab = sheet.worksheet(tab_name)

    # gets last un-updated row in column B
    last_row = len(tab.col_values(2))

    # if fresh sheet, adds header
    if last_row == 0:
        # sets base header list
        header_list = ["current_id"]

        # creates header list based on user selections
        if volume == True:
            header_list.append("volume_um3")
        if cable_length == True:
            header_list.append("cable_length")
        if synapse_counts == True:
            header_list += ["inc_syn", "out_syn", "total_syn"]
        if proofreading == True:
            header_list.append("proofread")

        # adds header list to sheet
        tab.update([header_list], "B1")

        # increments last row to 1 to start analysis
        last_row += 1

    # gets list of seg ids to get details for
    stale_ids = list(map(int, tab.col_values(1)[last_row:]))

    # gets requested details for each seg id and add to sheet
    for seg_id in stale_ids:

        # gets fresh seg ID
        try:
            fresh_seg = get_current_seg_id(datastack=datastack, seg_id=seg_id)
        except:
            try:
                fresh_seg = get_current_seg_id(datastack=datastack, seg_id=seg_id)
            except:
                fresh_seg = "ERROR"

        # creates output row using fresh seg id
        out_row = [str(fresh_seg)]

        # gets volume and add to output row if requested
        if volume == True:
            try:
                vol = float(
                    get_seg_3d_volume(
                        datastack=datastack,
                        seg_id=fresh_seg,
                    )
                )
            except:
                try:
                    vol = float(
                        get_seg_3d_volume(
                            datastack=datastack,
                            seg_id=fresh_seg,
                        )
                    )
                except:
                    vol = "ERROR"
            out_row.append(vol)

        # gets cable_length and add to output row if requested
        if cable_length == True:
            try:
                cable = get_cable_lengths(
                    datastack=datastack,
                    seg_ids=[fresh_seg],
                )[0]
            except:
                try:
                    cable = get_cable_lengths(
                        datastack=datastack,
                        seg_ids=[fresh_seg],
                    )[0]
                except:
                    cable = "ERROR"
            out_row.append(cable)

        # gets synapse data and add to output row if requested
        if synapse_counts == True:
            try:
                synapses = count_synapses(
                    datastack=datastack,
                    seg_ids=[fresh_seg],
                    detailed_results=True,
                )[int(fresh_seg)]
                inc = synapses["in"]
                out = synapses["out"]
                total = synapses["all"]
            except:
                try:
                    synapses = count_synapses(
                        datastack=datastack,
                        seg_ids=[fresh_seg],
                        detailed_results=True,
                    )[int(fresh_seg)]
                    inc = synapses["in"]
                    out = synapses["out"]
                    total = synapses["all"]
                except:
                    inc = "ERROR"
                    out = "ERROR"
                    total = "ERROR"
            out_row += [inc, out, total]

        # gets proofreading status and add to output row if requested
        if proofreading == True:
            try:
                proof = check_seg_proofread_status(datastack=datastack, seg_ids=[fresh_seg])[0]
            except:
                try:
                    proof = check_seg_proofread_status(datastack=datastack, seg_ids=[fresh_seg])[0]
                except:
                    proof = "ERROR"
            out_row.append(proof)

        # adds out row to sheet on first empty cell in column B
        tab.update([out_row], "B" + str(last_row + 1))

        # increments last row counter for next loop iteration
        last_row += 1


def gsheet_get_col_as_list(sheet_key, tab_name, col_num=1, ignore_header=False):
    """
    Gets data from a column in a google sheet as a list.

    This function requires a Google authentication token to be set up prior to use.
    The process for doing so is explained here: https://docs.gspread.org/en/latest/oauth2.html#oauth-client-id

    Args:
        sheet_key (str):
            the key for the google sheet to be updated, found in the url between '/d/' and '/edit?'
        tab_name (str):
            the name of the google sheet tab the list of IDs are in
            "tab" is an informal term, officially these are called "worksheets" within Google's documentation
        col_num (int, optional, default=1):
            the number of the column you want to convert
            column numbers start at 1 for column A, which is the default
        ignore_header (bool, optional, default=False):
            if True, will skip the first row of the column

    Returns:
        col (list):
            a list of the values in the column
    """

    # sets up google authentication using token
    gc = gspread.oauth()

    # creates gsheet object using sheet key
    sheet = gc.open_by_key(sheet_key)

    # creates worksheet object using tab name
    tab = sheet.worksheet(tab_name)

    # creates list of column values using column number
    col = tab.col_values(col_num)

    # pops first value if ignore header is true
    if ignore_header == True:
        col.pop(0)

    return col


def gsheet_get_tab_as_df(sheet_key, tab_name, has_headers=True):
    """
    Gets the data from a google sheet tab as a dataframe.

    This function requires a Google authentication token to be set up prior to use.
    The process for doing so is explained here: https://docs.gspread.org/en/latest/oauth2.html#oauth-client-id

    Args:
        sheet_key (str):
            the key for the google sheet to be updated, found in the url between '/d/' and '/edit?'
        tab_name (str):
            the name of the google sheet tab the list of IDs are in
            "tab" is an informal term, officially these are called "worksheets" within Google's documentation
        has_headers (bool, optional, default=True):
            whether or not the original data includes headers
            if set to False, will generate numeric column names automatically
            this avoids first row being used for dataframe column names

    Returns:
        df (pandas DataFrame object):
            a dataframe of the values from the submitted spreadsheet tab
    """

    # sets up google credentials
    gc = gspread.oauth()

    # opens sheet as object using sheet key
    sheet = gc.open_by_key(sheet_key)

    # sets the tab you want to update using tab name
    tab = sheet.worksheet(tab_name)

    # makes output for data requiring header generation
    if has_headers == False:
        data = tab.get_all_values()
        df = pd.DataFrame(
            data, columns=["col_" + str(i + 1) for i in range(len(data[0]))]
        )
    # makes output for data that already has headers
    else:
        df = pd.DataFrame(tab.get_all_records())

    return df


def host_ng_volume_locally(volume_path):
    """
    Hosts a volume of meshes on a local server for testing using cloudvolume. 
    
    Run this function to start the host server, see readme for more detailed instructions.

    Args:
        volume_path (str):
            the absolute path to folder of the neuroglancer volume that contains the mesh to host
            e.g. '/home/username/ng_meshes/image'
    """

    # removes trailing slashes from filepath if present
    if volume_path[-1] == "/":
        volume_path = volume_path[:-1]

    # creates cloudpath using volume path
    cloud_path = "file://" + volume_path

    # creates a cloudvolume object using cloud path
    try:
        volume = cloudvolume.CloudVolume(cloud_path)
    # handles bad directory input
    except FileNotFoundError:
        print(
            f"The directory '{cloud_path}' couldn't be found. Please check the accuracy of this filepath."
        )
    # handles all other errors
    except Exception as e:
        print(f"An error occurred: {e}")

    # runs a local server that hosts the volume
    volume.viewer()


def make_anno_layer(
    datastack,
    annotations,
    layer_type,
    layer_name,
    descriptions=[],
    linked_segs=[],
    linked_seg_layer_name=None,
):
    """
    Converts a list of annotations into a neuroglancer-format dictionary for an annotation layer.

    Args:
        datatack (str):
            the name of the datastack the annotations are for 
            e.g. "brain_and_nerve_cord"
        annotations (list):
            a list of all the annotations formatted correctly for the type
            structure varies depending on annotation type (point, line, etc.)
        layer_type (str):
            the type of annotations in the layer
            supported types are "point", "line", "bbox", "sphere"/"ellipsoid", "polyline", and "mixed"
        layer_name (str):
            the name you want the layer to have in neuroglancer
        descriptions (list of str, optional, default=[]):
            list of annotation descriptions, length must match list of annotations
        linked_segs (list, optional, default=[]):
            list of segment IDs to link annotations to, must be same length as list of annotations
            structure varies based on what type of annotation is used
        linked_seg_layer_name (str, optional, default=None):
            the name of the segmentation layer if one is to be linked tot he annotations

    Returns:
        anno_layer_dict (dict):
            dictionary for an annotation layer of the appropriate type
            structured to work with neuroglancer state json format
    """

    if len(linked_segs) > 0 and linked_seg_layer_name == None:
        raise Exception(
            "If linked segmentation is passed, you must also pass the name of the segmentation layer to be linked using the linked_seg_layer_name argument."
        )

    # makes an empty list to fill with annotation dictionaries
    anno_dict_list = []

    # creates numbering variable for annotation id assignment
    id_num = 0

    # populates anno_dict_list with annotation dicts
    for entry_index, entry in enumerate(annotations):
        # handles mixed annotation layers
        if layer_type == "mixed":
            anno = entry[0]
            anno_type = entry[1]
        # handles monotype layers
        else:
            anno = entry
            anno_type = layer_type

        # adds one to id_num to create layer-unique id for this annotation
        id_num += 1

        # appends correctly-formatted dict for each annotation
        if anno_type == "point":
            anno_dict_list.append(
                {
                    "point": anno,
                    "type": "point",
                    "id": str(id_num),
                }
            )
        elif anno_type == "line":
            anno_dict_list.append(
                {
                    "pointA": anno[0],
                    "pointB": anno[1],
                    "type": "line",
                    "id": str(id_num),
                }
            )
        elif anno_type == "bbox":
            anno_dict_list.append(
                {
                    "pointA": anno[0],
                    "pointB": anno[1],
                    "type": "axis_aligned_bounding_box",
                    "id": str(id_num),
                }
            )
        elif anno_type == "sphere" or anno_type == "ellipsoid":
            anno_dict_list.append(
                {
                    "center": anno[0],
                    "radii": anno[1],
                    "type": "ellipsoid",
                    "id": str(id_num),
                }
            )
        elif anno_type == "polyline":
            anno_dict_list.append(
                {
                    "points": anno,
                    "type": "polyline",
                    "id": str(id_num),
                }
            )
        # handles bad type annotation types
        else:
            if layer_type != "mixed":
                raise ValueError(
                    f"The value '{layer_type}' is invalid for the 'layer_type' argument. It must be one of the following: 'point', 'line', 'bbox', 'sphere' or 'ellipsoid' (these two return the same result), 'polyline', or 'mixed'."
                )
            else:
                raise ValueError(
                    f"The value '{anno_type}' is invalid for the annotation type of annotation at index {entry_index}. It must be one of the following: 'point', 'line', 'bbox', 'sphere' or 'ellipsoid' (these two return the same result), or 'polyline'."
                )

    # handles descriptions and linked segmentation
    for i, anno_dict in enumerate(anno_dict_list):

        # adds annotation descriptions if passed
        if len(descriptions) > 0:
            anno_dict["description"] = descriptions[i]

        # adds linked segmentation ids if passed
        if len(linked_segs) > 0:
            if type(linked_segs[0]) == list:
                anno_dict["segments"] = [list(map(str, linked_segs[i]))]
            else:
                anno_dict["segments"] = [str(linked_segs[i])]

    # gets config for chosen datastack
    config = get_config(datastack=datastack)

    # sets voxel scale dimensions using config
    dims = {
        "x": [config["resolution"][0] * 1e-9, "m"],
        "y": [config["resolution"][1] * 1e-9, "m"],
        "z": [config["resolution"][2] * 1e-9, "m"],
    }

    # make output layer dict
    anno_layer_dict = {
        "annotations": anno_dict_list,
        "name": layer_name,
        "source": {
            "transform": {"outputDimensions": dims},
            "url": "local://annotations",
        },
        "tab": "annotations",
        "type": "annotation",
    }

    # turns on linked segmentation if requested
    if len(linked_segs) > 0:
        anno_layer_dict["linkedSegmentationLayer"] = {"segments": linked_seg_layer_name}
        anno_layer_dict["filterBySegmentation"] = ["segments"]

    return anno_layer_dict


def make_bucket_volume_from_obj(datastack, obj_path, bucket_path):
    """
    Converts a locally-stored OBJ file into a neuroglancer volume on a remote cloudfiles-managed bucket.
    
    Mesh will be Neuroglancer legacy-format single-resolution precomputed.

    CURRENTLY ONLY WORKS FOR BANC DATASET
    This function requires that you have write access to the bucket where you're creating the volume.
    It's built using cloudfiles and cloudvolume, documentation for which can be found at
    https://pypi.org/project/cloud-files and https://pypi.org/project/cloud-volume respectively.

    Args:
        datastack (str):
            the name of the datastack the OBJ is set up for
            e.g. "brain_and_nerve_cord"
        obj_path (str):
            the absolute path to the OBJ file on your local machine
            e.g. "/home/username/obj_meshes/my_mesh.obj"
        bucket_path (str):
            the absolute path to the folder where you want the NG volume on the bucket
            must end in the name of the folder you want the to contain the volume
            will create new folders where none exist
            e.g. "server://bucket/my_project/neuron_mesh_01"
    """

    # sets coordinate resolution and chunk size for volume
    resolution = [1, 1, 1]
    chunk_size = [512, 512, 16]  # will need to be generalized using config #

    # gets config info dict for chosen datastack
    try:
        config = get_config(datastack=datastack)
    except KeyError:
        raise KeyError(
            "The datastack name is invalid. To see a list of currently-supported datastack names, use the get_supported_configs() function."
        )

    # pulls voxel xyz dimensions from config dict
    resolution = config["resolution"]

    # gets volume size from config
    volume_size = config["volume_size"]

    # imports obj as trimesh mesh
    obj_mesh = trimesh.load(obj_path)

    # creates bucket paths for image and mesh folder
    image_path = bucket_path
    mesh_path = image_path + "/mesh"

    # creates cloudfiles objects for volume image and mesh folders using bucket paths
    image_cf = CloudFiles(image_path)
    mesh_cf = CloudFiles(mesh_path)

    # sets content for cloudvolume image info file
    image_info = cloudvolume.CloudVolume.create_new_info(
        num_channels=1,
        layer_type="segmentation",
        data_type="uint64",  # Channel images might be 'uint8'
        encoding="raw",  # encoding options are raw, png, jpeg, compressed_segmentation, fpzip, kempressed, zfpc, compresso, crackle #
        resolution=resolution,
        voxel_offset=[0, 0, 0],  # x,y,z offset in voxels from the origin #
        mesh="mesh",
        # Pick a convenient size for your underlying chunk representation #
        # Powers of two are recommended, doesn't need to cover image exactly #
        chunk_size=chunk_size,
        volume_size=volume_size,
    )

    # sets content for precomputed legacy unsharded mesh info file
    mesh_info = {
        "@type": "neuroglancer_legacy_mesh",
        "transform": [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    }

    # adds volume info file to bucket
    image_cf.put("info", json.dumps(image_info))

    # adds mesh info file to bucket
    mesh_cf.put("info", json.dumps(mesh_info))

    # creates cloudvolume object using bucket image path
    volume = cloudvolume.CloudVolume(image_path)

    # creates cloudvolume mesh object using trimesh mesh
    cv_format_mesh = cloudvolume.Mesh(vertices=obj_mesh.vertices, faces=obj_mesh.faces)

    # gives the mesh a segment id of 1
    cv_format_mesh.segid = 1

    # adds the mesh into the volume's list of meshes,
    # generates two files in 'mesh' folder
    # one named '1:0', called the manifest file and
    # one named "1:0:1.gz", called the fragment file #
    volume.mesh.put(cv_format_mesh)


def make_color_list(number_of_colors, alternate_brightness=0.0):
    """
    Generates a list of hex values spread around a color wheel based on the number requested.

    Useful for visually distinguishing multiple segments or annotation layers.
    Uses slightly desaturated colors, avoids colors near "true blue" (#0000FF) which can be harsh on eyes over time.
    Optionally vary the brightness of nearby colors if it starts getting crowded.

    Args:
        number_of_colors (int)
            the number of segments you need colors for
        alternate_brightness (float, optional, default=0.0):
            value between 0 and 1 indicating how much to vary the brightness of neighboring colors
            values close 0 will produce mild variation, those near 1 will approach black and white
            only affects lists of 11 or more colors

    Returns:
        colors (list of str): 
            a list of the requested number of color-wheel-spaced hex values
    """

    # handles input if alternate_brightness is outside the range 0 to 1
    if alternate_brightness < 0 or alternate_brightness > 1:
        raise ValueError("alternate_brightness must be a value between 0.0 and 1.0.")

    # sortens number_of_colors to n for simplicity
    n = number_of_colors

    # hard coded default color list for numbers of segments <= 10
    default_list = [
        "#FF5533", # red #
        "#FF9C33", # orange #
        "#FFDD33", # yellow #
        "#B9DA00", # yellow-green #
        "#A8FFA8", # green #
        "#00A870", # blue-green #
        "#B0FEFF", # cyan #
        "#469FE3", # blue #
        "#CC85FF", # purple #
        "#FF40DF", # magenta #
    ]

    # determines colors if 10 or fewer segments
    if n == 1:
        return [default_list[2]]  # returns yellow for single-id cases #
    elif n == 2:
        colors = [default_list[i] for i in [0, 7]]  # red and blue #
    elif n == 3:
        colors = [default_list[i] for i in [0, 2, 7]]  # add yellow #
    elif n == 4:
        colors = [default_list[i] for i in [0, 2, 4, 7]]  # add green #
    elif n == 5:
        colors = [default_list[i] for i in [0, 2, 4, 7, 8]]  # add purple
    elif n == 6:
        colors = [default_list[i] for i in [0, 1, 2, 4, 7, 8]]  # add orange #
    elif n == 7:
        colors = [default_list[i] for i in [0, 1, 2, 4, 7, 8, 9]]  # add magenta #
    elif n == 8:
        colors = [default_list[i] for i in [0, 1, 2, 4, 6, 7, 8, 9]]  # add cyan #
    elif n == 9:
        colors = [
            default_list[i] for i in [0, 1, 2, 3, 5, 6, 7, 8, 9]
        ]  # split green into yellow- and blue-green #
    elif n == 10:
        colors = default_list

    # determines colors mathematically if more than 10 segments
    elif n > 10:
        # sets starting positions on hue wheel
        current_pos = 0
        # determines increment based on max steps of 1530 / number of steps needed
        increment = int((1530) / n)
        # makes list of positions to fill starting with true red at 0
        positions = [0]
        # fills position list by adding increment to current position
        for x in range(n - 1):
            current_pos += increment
            positions.append(current_pos)
        # makes emtpy list to fill with rgb values
        rgb_colors = []
        # generates rgb value list for each position by moving around color wheel
        for position in positions:
            if position <= 255:
                rgb = [255, position, 0]  # increase green #
            elif position <= 510:
                inc = position - 255
                rgb = [255 - inc, 255, 0]  # decrease red #
            elif position <= 765:
                inc = position - 510
                rgb = [0, 255, inc]  # increase blue #
            elif position <= 1020:
                inc = position - 765
                rgb = [0, 255 - inc, 255]  # decrease green #
            elif position <= 1275:
                inc = position - 1020
                rgb = [inc, 0, 255]  # increase red #
            elif position <= 1530:
                inc = position - 1275
                rgb = [255, 0, 255 - inc]  # decrease blue #
            rgb_colors.append(rgb)

        # creates functions to darken or lighten colors
        def _darken(rgb):
            dark_rgb = []
            for channel in rgb:
                dark_rgb.append(int(channel * (1 - alternate_brightness)))
            return dark_rgb
        def _lighten(rgb):
            light_rgb = []
            for channel in rgb:
                dif = 255 - channel
                light_rgb.append(int(channel + alternate_brightness * dif))
            return light_rgb

        # creates empty list to fill with modified colors
        new_colors = []

        # creates counter based on number of colors
        counter = n

        # if there are an odd number of colors handles first color manually without adjustment
        if n % 2 != 0:
            new_colors.append(rgb_colors[0])
            counter -= 1
            del rgb_colors[0]

        # alternates between darkening and lightening each color in list
        for color in rgb_colors:
            if counter % 2 == 0:
                new_colors.append(_darken(color))
                counter -= 1
            else:
                new_colors.append(_lighten(color))
                counter -= 1

        # sets rgb_colors equal to modified list
        rgb_colors = new_colors

        # converts rgb to hex using string formatting
        colors = [
            "#"
            + "{:02x}".format(color[0])
            + "{:02x}".format(color[1])
            + "{:02x}".format(color[2])
            for color in rgb_colors
        ]

    # raises error when users input negative numbers or non-integers
    else:
        raise ValueError("number_of_colors argument must be a positive integer.")

    return colors

def make_edits_link(datastack, seg_id, separate_layers=False):
    """
    Make a neuroglancer link with all the edits to a given segment as line annotations.

    Args:
        datastack (str):
            the name of the CAVEdatastack the segment ID is from
            e.g. "brain_and_nerve_cord"
        seg_id (int):
            a segment ID to build the edit link for
    """

    # sets client using datastack name
    client = CAVEclient(datastack)

    # gets tracer config dict
    config = get_config(datastack=datastack)

    # pulls voxel resolution from tracer config_dict
    res = config["resolution"]

    # creates df of all edits
    change_df = get_seg_edits(datastack=datastack, seg_id=seg_id)

    # determines the original seg ID
    first_before = change_df.loc[0, "before_segs"]

    # if first operation is a split, uses initial ID as original
    if len(first_before) == 1:
        original_seg = first_before[0]

    # if first operation is a merge, chooses best original ID candidate by
    # checking which initial ID shares more supervoxels with the final ID
    elif len(first_before) == 2:

        # gets supervoxels of final ID
        end_svs = client.chunkedgraph.get_leaves(root_id=seg_id)

        # gets seg ids from initial merge
        seg_a, seg_b = first_before

        # gets supervoxels for each candidate
        a_svs = client.chunkedgraph.get_leaves(root_id=seg_a)
        b_svs = client.chunkedgraph.get_leaves(root_id=seg_b)

        # calculates number of svs that overlap between candidates and final
        a_overlap = sum(i in a_svs for i in end_svs)
        b_overlap = sum(i in b_svs for i in end_svs)

        # sets original ID based on which candidate shares more with final
        if a_overlap > b_overlap:
            original_seg = first_before[0]
        elif b_overlap > a_overlap:
            original_seg = first_before[1]

    # defines function to make annotation layers specific to this linkbuilder
    def _make_layers(datastack, df, res, linked=True, layer_name="Edits"):
        """
        Make an annotation layer specific to this function.

        Args:
            datastack (str):
                the name of the datastack
            df (pandas DataFrame object):
                the dataframe of edits to turn into an annotation layer 
            res (list of 3 ints):
                the voxel resolution of the datastack, e.g. [4,4,45] 
            linked (bool, optional, default=True)
                if True, will add additional layer with linked segmentation 
            layer_name (str, optional, default=Edits):
                the name to use for the annotation layer
                linked segmentation layer will appear as linked_ + layer_name

        Returns:
            layers (list of dicts):
                a list of spelunker-formatted annotation layer dictionaries 
        """

        # gets coords from df as list
        coords = df["coords"].values.tolist()

        # converts coord x and y dims, leave z alone
        # odd but necessary for using coords pulled from operation dict
        coords = [
            [[xyz[0] * res[0], xyz[1] * res[1], xyz[2]] for xyz in coord]
            for coord in coords
        ]

        # gets segment pair from df
        linked_segs = df["root_pair"].values.tolist()

        # makes empty list to fill with anno descriptions
        descriptions = []

        # iterates through df rows to build descriptions
        for i, row in df.iterrows():

            # gets operation id and convert to string
            oid = str(row["operation_id"])

            # determines operation type
            is_merge = row["is_merge"]
            if is_merge == True:
                opname = "Merge"
            elif is_merge == False:
                opname = "Split"

            # gets user id and convert to string
            user = str(row["user"])

            # constructs decription string and add to list
            desc = opname + " by user " + user + ", Operation ID: " + oid
            descriptions.append(desc)

        # creates unlinked layer
        unlinked_layer = make_anno_layer(
            datastack=datastack,
            annotations=coords,
            layer_type="line",
            layer_name=layer_name,
            descriptions=descriptions,
        )

        # makes layers list and add unlinked layer
        layers = [unlinked_layer]

        # if linked layer requested, makes and adds to layers list
        if linked == True:
            linked_layer = make_anno_layer(
                datastack=datastack,
                annotations=coords,
                layer_type="line",
                layer_name="Linked " + layer_name,
                descriptions=descriptions,
                linked_segs=linked_segs,
                linked_seg_layer_name="Segmentation",
            )
            layers.append(linked_layer)

        return layers

    # layer creation if only one layer is chosen
    if separate_layers == False:
        anno_layers = _make_layers(datastack, change_df, res)

    # layer creation if separate split and merge layers are selected
    elif separate_layers == True:

        # splits change_df into merge and split dfs on is_merge column
        merge_df = change_df[change_df["is_merge"]]
        split_df = change_df[change_df["is_merge"] == False]

        # merge and split annotation layer lists
        # includes unlinked and linked layer for each
        merge_layers = _make_layers(datastack, merge_df, res, layer_name="Merges")
        split_layers = _make_layers(datastack, split_df, res, layer_name="Splits")

        # adds color coding for split layers
        merge_layers[0]["annotationColor"] = "#00ffff"  # cyan #
        split_layers[0]["annotationColor"] = "#ff0000"  # red #

        # combines merge and split layer lists into one list
        anno_layers = merge_layers + split_layers

    # builds final output link
    link = make_ng_link(
        datastack=datastack,
        seg_ids=[seg_id, original_seg],
        anno_layers=anno_layers,
        region_meshes=False,
        seg_colors=["#00ffff", "#ff0000"],  # sets original seg to red, final to cyan #
        translucent_seg=True,  # makes segs translucent to grey out overlap #
    )

    return link


def make_local_volume_from_obj(datastack_name, obj_path, output_path):
    """
    Generates a local neuroglancer volume that contains a single-resolution precomputed mesh using an OBJ file. 
    
    Doesn't currently work on Windows due to unavoidable use of colons in several filenames.

    Args:
        datastack_name (str):
            the name of the datastack the OBJ mesh is from, e.g. 'brain_and_nerve_cord'
            for a list of currently-supported datastacks use get_supported_configs()
        obj_path (str):
            the absolute filepath to the NG state JSON file to pull annotations from
            e.g. '/home/username/ng_jsons/state.json'
        output_path (str):
            the absolute path to the folder where you want to save the mesh output
            e.g. '/home/username/ng_meshes'
            the volume folder called "image" will be created in this folder
    """

    # gets config info dict for chosen datastack
    try:
        config = get_config(datastack=datastack_name)
    except KeyError:
        raise KeyError(
            "The datastack name is invalid. To see a list of currently-supported datastack names, use the get_supported_configs() function."
        )

    # pulls voxel xyz dimensions from config dict
    resolution = config["resolution"]

    # imports obj as trimesh object
    obj_mesh = trimesh.load(obj_path)

    # creates a folder inside the specified directory called '/image' and adds
    # an info file to it, then creates a subfolder inside image called '/mesh'
    # and adds another info file to that. This is the necessary file structure
    # for cloudvolume to create a legacy-format unsharded single-resolution mesh
    make_volume_packaging(resolution=resolution, output_filepath=output_path)

    # constructs cloudpath from filepath
    cloudpath = "file://" + output_path + "/image"

    # creates cloudvolume object using information at cloudpath
    volume = cloudvolume.CloudVolume(cloudpath)

    # makes a cloudvolume mesh using the trimesh object
    cv_format_mesh = cloudvolume.Mesh(vertices=obj_mesh.vertices, faces=obj_mesh.faces)

    # gives the mesh a segment id of 1
    cv_format_mesh.segid = 1

    # adds the mesh into the volume's list of meshes, generating two files in
    # the '/image/mesh' folder, one named '1:0', called the manifest file, and
    # the other named "1:0:1.gz", called the fragment file
    volume.mesh.put(cv_format_mesh)


def make_mesh_from_points(
    datastack,
    share_url,
    bucket_path,
    alphas=None,
    auto_grow=True,
    save_objs=False,
    obj_path=None,
    print_alphas=False,
):
    """
    Generates a bucket-hosted NG mesh from a shortlink of point annotations and returns a shortlink to it.

    !!!WARNING!!!: This function is extremely experimental and may break easily. 
    Currently only works with BANC dataset and hosting from nokura princeton server
    Generates a neuroglancer legacy-format volume with one single-resolution unsharded mesh made by combining
    all the point annotation layers within a neuroglancer json state pulled from a shortened spelunker-format 
    state url, uploads this volume to a bucket, and generates a neuroglancer link to the result.
    Optionally save the submeshes created for each layer and the final mesh as OBJ files.

    Args:
        datastack (str):
            the name of the datastack the state url is from
            e.g. 'brain_and_nerve_cord'
            for a list of currently-supported datastacks use get_supported_configs()
        share_url (str):
            the shortened spelunker url of a NG state
        bucket_path (str):
            the absolute filepath where you want the volume to be hosted on a bucket
            last folder name will be the volume folder
            will create new folders where none exist
        alphas (list of floats or ints, optional, default=None):
            the alpha shape values you want to use for each submesh made from a point annotation layer
            length must match number of point annotation layers in share url
            passing an alpha value of None will attempt to generate one automatically
            the default value of None sets all the individual list values to None
        auto_grow (bool, optional, default=True):
            default value of True allows for iterative increase of alpha until a watertight mesh is produced
            if set to False, will only try first alpha value for each submesh, which is prone to failure
        save_objs (bool, optional, default=False):
            if True, will save an OBJ file for each of the submeshes and the final mesh
            saves in location specified by obj_path argument
        obj_path (str, optional, default=None):
            the absolute path to the folder where you want OBJ files produced by the save_objs=True toggle
            default value of None attempts to find default home/Downloads folder
        print_alphas (bool, optional, default=False):
            if set to True, will print out starting and ending alpha values for each submesh
            useful for testing and troubleshooting

    Returns:
        link (str):
            the shortened link to the spelunker NG state containing the final mesh
            includes all the annotation layers that created it for inspecting accuracy
            mesh layer name includes final alpha values used for each submesh

        In addition to returning the link, this function also saves a neuroglancer legacy-format volume
        containing a single-resolution mesh on the specified bucket. This is required to generate the link,
        as it serves aas the host for the mesh layer. It also optionally saves OBJ files
        for each submesh and the final mesh if the save_objs argument is set to True.
    """

    # sets coordinate resolution and chunk size for volume
    chunk_size = [512, 512, 16] 

    # sets client using datastack name
    client = CAVEclient(datastack)

    # splits share url into components between slashes
    split_url = share_url.split("/")

    # gets state ID, which is always last component
    state_id = int(split_url[-1])

    # retreives JSON from state server using state ID
    json_dict = client.state.get_state_json(state_id)

    # gets config info dict for chosen datastack
    try:
        config = get_config(datastack=datastack)
    except KeyError:
        raise KeyError(
            "The datastack name is invalid. To see a list of currently-supported datastack names, use the get_supported_configs() function."
        )

    # pulls voxel xyz dimensions from config dict
    resolution = config["resolution"]

    # makes empty list to fill with annotation layer names
    layer_names = []

    # selectively gets layer names from state json file
    for layer in json_dict["layers"]:
        # avoids archived and hidden layers
        if "archived" not in layer:
            if "visible" not in layer:
                # avoids non-annotation layers
                if layer["type"] == "annotation":
                    # avoids empty annotation layers
                    if len(layer["annotations"]) > 0:
                        # avoids non-point annotation layers
                        if layer["tool"] == "annotatePoint":
                            layer_names.append(layer["name"])

    # makes empty list to fill with point arrays
    point_arrays = []

    # iterates through layer names and generates an obj for each
    for layer_name in layer_names:

        # searches the full dict for the annotation layer specified and pulls it out as a separate list
        for layer in json_dict["layers"]:
            if layer["name"] == layer_name:
                anno_raw_list = layer["annotations"]

        # creates an empty list to fill with points
        points = []

        # pulls the actual coordinate info out of the layer list
        for anno in anno_raw_list:
            points.append(anno["point"])

        # converts points list to numpy array
        points = np.array(points)

        # converts coords to numpy array of nm-resolution point coord numpy arrays
        nm_points = np.array(
            [
                convert_coord_res(
                    point_coords=point, res_current=resolution, res_desired=[1, 1, 1]
                )
                for point in points
            ]
        )

        # adds point array to list
        point_arrays.append(nm_points)

    # makes empty list to populate with meshes
    meshes = []

    # if no alpha list passed, generates list of None values matched to length of meshes
    if alphas == None:
        alphas = [None for points in point_arrays]

    # makes empty list to fill with point clouds for anno layers
    point_clouds = []

    # makes empty list to fill with chosen alpha values
    chosen_alphas = []

    # sets counter for alpha printouts #
    alpha_count = 1

    # generates mesh for each points annotation layer in json state
    for points, alpha in zip(point_arrays, alphas):

        # makes version of points in viewer resolution for final link anno layer
        # appends to list of point clouds
        point_clouds.append(
            [[point[0] / 4, point[1] / 4, point[2] / 45] for point in points]
        )

        # defines function to generate list of verts, faces, and alpha value for mesh
        def _alpha_shape_3d(points, alpha=None, auto_grow=True, max_iters=15):
            """3D alpha shape (concave hull) via Delaunay tetrahedralization."""

            # ensures points are formatted as array of floats
            points = np.asarray(points, dtype=float)

            # uses Delaunay "triangulation" to generate "triangulation" map
            # tess is a Delaunay object made of "simplices" (triangles in 2D)
            # Delaunay objects made from 3D coords will generate tetrahedron simplices
            # simplices are stored as index numbers of vertices in original list
            # https://thearn.github.io/docs/generated/scipy.spatial.Delaunay.html
            # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Delaunay.html
            tess = Delaunay(points)

            # gets numpy array of simplices from Delaunay object
            tets = points[tess.simplices]

            def _tet_circumradii(tetras):

                # makes array of first vertex in each tetra
                p0 = tetras[:, 0]
                # makes array of directed a-vectors from second to first vertices
                a = tetras[:, 1] - p0
                # makes array of directed b-vectors from third to first vertices
                b = tetras[:, 2] - p0
                # makes array of directed c-vectors from fourth to first vertices
                c = tetras[:, 3] - p0

                # makes new array with columns for a-, b-, and c-vectors
                # this serves as the coefficient matrix
                A = np.stack([a, b, c], axis=1)

                # makes a new array with columns for the sum of the squared vector distances for each vector
                # each row corresponds to a tetra's halved [a-vector square sum, b..., c...]
                # this is called the right-hand (Riemann) sum
                rhs = 0.5 * np.stack(
                    [(a * a).sum(1), (b * b).sum(1), (c * c).sum(1)], axis=1
                )

                try:
                    # tries to use linear algebra solver to get solution vector x
                    # feeds in coefficient matrix A and constant vector (normally called b) based on right-hand sums
                    x = np.linalg.solve(A, rhs[..., None])[..., 0]
                except np.linalg.LinAlgError:
                    x = np.zeros_like(rhs)
                    for i in range(A.shape[0]):
                        try:
                            x[i] = np.linalg.solve(A[i], rhs[i])
                        except np.linalg.LinAlgError:
                            x[i] = np.full(3, np.inf)
                return np.linalg.norm(x, axis=1)

            radii = _tet_circumradii(tetras=tets)

            if alpha is None:
                kd = cKDTree(points)
                nn_dist, _ = kd.query(points, k=2)
                alpha = 1.5 * float(np.median(nn_dist[:, 1]))

            def _alpha_shape_once(points, tess, radii, alpha):
                keep = tess.simplices[radii < alpha]
                if len(keep) == 0:
                    return None, None, 0
                face_counter = Counter()
                for tet in keep:
                    for combo in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)):
                        face_counter[tuple(sorted(int(tet[i]) for i in combo))] += 1
                faces = np.array(
                    [f for f, c in face_counter.items() if c == 1], dtype=np.int64
                )
                if len(faces) == 0:
                    return None, None, len(keep)
                used = np.unique(faces.ravel())
                remap = -np.ones(len(points), dtype=np.int64)
                remap[used] = np.arange(len(used))
                return points[used], remap[faces], len(keep)

            # if auto_grow is set to False, only uses the first alpha value for each submesh and stops
            if not auto_grow:
                v, f, _ = _alpha_shape_once(points, tess, radii, alpha)
                if v is None:
                    raise ValueError(
                        f"alpha={alpha:.1f} produced no boundary triangles."
                    )
                return v, f, alpha

            single_piece = None
            cur_alpha = alpha

            for _ in range(max_iters):
                v, f, _ = _alpha_shape_once(points, tess, radii, cur_alpha)
                if v is None:
                    cur_alpha *= 1.5
                    continue
                m = trimesh.Trimesh(vertices=v, faces=f, process=False)
                if m.body_count == 1:
                    if single_piece is None:
                        single_piece = (v, f, cur_alpha)
                    if m.is_watertight:
                        m.fix_normals()
                        return np.asarray(m.vertices), np.asarray(m.faces), cur_alpha
                cur_alpha *= 1.5

            if single_piece is None:
                raise ValueError(
                    f"alpha shape failed to produce a single-component mesh up to {cur_alpha:.1f}."
                )

            return single_piece

        # sets vertices, faces, and alpha value using alpha_shape_3d function
        v, f, a = _alpha_shape_3d(points, alpha=alpha, auto_grow=auto_grow)

        # prints out intitial and final alpha values for troubleshooting output
        if print_alphas == True:
            print("Submesh", str(alpha_count), "alpha value", alpha, "to", a)
            alpha_count += 1

        # adds whatever alpha value was used to chosen list
        chosen_alphas.append(a)

        # generates a trimesh object using vertices and faces
        submesh = trimesh.Trimesh(vertices=v, faces=f, process=False)

        # adds each mesh to the list of meshes
        meshes.append(submesh)

    # merges all submeshes into final mesh using manifold3d engine boolean union
    # boolean operations only work on watertight manifold solids with positive volume
    mesh = trimesh.boolean.boolean_manifold(meshes=meshes, operation="union")

    # prints warning message if final mesh isn't watertight
    if mesh.is_volume != True:
        print("Final mesh is not a watertight manifold solid with postitive volume.")

    # handles obj save behavior if requested
    if save_objs == True:

        # tries to get the user's Downloads folder path if none specified #
        if obj_path == None:
            try:
                obj_path = str(Path.home() / "Downloads")
            except:
                raise Exception(
                    "Default download folder couldn't be found, please specify the absolute file path to a folder using the 'obj_path' argument."
                )

        # adds trailing slash if not present
        if obj_path[-1] != "/":
            obj_path += "/"

        # makes list of all submeshes and final mesh
        export_meshes = meshes + [mesh]

        # names and exports each mesh
        for i in range(len(export_meshes)):

            # handles naming difference for submeshes and final mesh
            if i < len(export_meshes) - 1:
                # creates obj export path from output_path
                subpath = obj_path + "submesh_" + str(i + 1) + ".obj"
            else:
                subpath = obj_path + "final_mesh.obj"

            # saves mesh as obj file at output path location
            export_meshes[i].export(subpath, file_type="obj")
        
        # currently unused
        # except:
        #     raise Exception("OBJ save process failed.")

    # calculates centerpoint from mesh boundaries
    centerpoint = list(map(int, np.mean(mesh.bounds, axis=0)))

    # converts centerpoint from nm to volume resolution
    centerpoint = convert_coord_res(
        point_coords=centerpoint, res_current=[1, 1, 1], res_desired=resolution
    )

    # gets volume size from config
    volume_size = config["volume_size"]

    # creates bucket paths for image and mesh folder
    image_path = bucket_path
    mesh_path = image_path + "/mesh"

    # creates cloudfiles objects for volume image and mesh folders using bucket paths
    image_cf = CloudFiles(image_path)
    mesh_cf = CloudFiles(mesh_path)

    # sets content for cloudvolume image info file
    image_info = cloudvolume.CloudVolume.create_new_info(
        num_channels=1,
        layer_type="segmentation",
        data_type="uint64",  # channel images might be 'uint8' #
        # encoding options are raw, png, jpeg, compressed_segmentation, fpzip, kempressed, zfpc, compresso, crackle #
        encoding="raw",  
        resolution=resolution,
        voxel_offset=[0, 0, 0],  # x,y,z offset in voxels from the origin #
        mesh="mesh",
        # pick a convenient size for your underlying chunk representation #
        # powers of two are recommended, doesn't need to cover image exactly #
        chunk_size=chunk_size,
        volume_size=volume_size,
    )

    # sets content for precomputed legacy unsharded mesh info file
    mesh_info = {
        "@type": "neuroglancer_legacy_mesh",
        "transform": [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    }

    # adds volume info file to bucket
    image_cf.put("info", json.dumps(image_info))

    # adds mesh info file to bucket
    mesh_cf.put("info", json.dumps(mesh_info))

    # creates cloudvolume object using bucket image path
    volume = cloudvolume.CloudVolume(image_path)

    # creates cloudvolume mesh object using trimesh mesh
    cv_format_mesh = cloudvolume.Mesh(vertices=mesh.vertices, faces=mesh.faces)

    # gives the mesh a segment id of 1
    cv_format_mesh.segid = 1

    # adds the mesh into the volume's list of meshes,
    # generates two files in 'mesh' folder
    # one named '1:0', called the manifest file and
    # one named "1:0:1.gz", called the fragment file #
    volume.mesh.put(cv_format_mesh)

    # gets post-nokura section of bucket path
    short_bucket_path = bucket_path[9:]

    # generates NG-format source url for bucket-hosted mesh
    mesh_source_url = (
        "https://c10s.pni.princeton.edu/"
        + short_bucket_path
        + "|neuroglancer-precomputed:"
    )

    # creates empty list to fill with annotation layers
    anno_layers = []

    # creates empty list to fill with anno layer names
    anno_layer_names = []

    # creates empty string to fill with mesh name using alpha values
    mesh_name = ""

    # generates anno and mesh layer names
    for i in range(len(chosen_alphas)):
        anno_layer_names.append("m" + str(i + 1))
        mesh_name += "m" + str(i + 1) + "a" + str(int(chosen_alphas[i])) + "_"

    # drops trailing underscore from mesh name
    mesh_name = mesh_name[:-1]

    # creates spelunker-format annotation layer to feed into link builder and add to list
    for point_cloud, layer_name in zip(point_clouds, anno_layer_names):
        anno_layer = make_anno_layer(
            datastack=datastack,
            annotations=point_cloud,
            layer_type="point",
            layer_name=layer_name,
        )
        anno_layers.append(anno_layer)

    # generates list of colors for annotation points based on number of layers
    colors = make_color_list(len(anno_layers))

    # sets colors of annotation layers based on number
    for layer, color in zip(anno_layers, colors):
        layer["annotationColor"] = color

    # makes NG link using original anno points and hosted mesh
    link = make_ng_link(
        datastack=datastack,
        anno_layers=anno_layers,
        custom_mesh_source=mesh_source_url,
        custom_mesh_name=mesh_name,
        view_coords=centerpoint,
    )

    return link


def make_ng_link(
    datastack,
    seg_ids=[],
    anno_layers=[],
    region_meshes=False,
    seg_colors=[],
    viewer_site="default",
    custom_mesh_source=None,
    custom_mesh_name=None,
    custom_mesh_color=None,
    view_coords=None,
    long_url=False,
    translucent_seg=False,
):
    """
    Generates a neuroglancer link from a datastack name, optionally adding a list of segment IDs and various layers. 
    
    For a list of currently-supported datastacks, use the get_datastack_names() function.

    Args:
        datastack (str):
            the name of the datastack to build a link for
            e.g. 'brain_and_nerve_cord'
        seg_ids (list of ints, optional, default=[]):
            the IDs of any segments you want included with the link
        anno_layers (list of dicts, optional, default=[]):
            a list of annotation layer dictionaries to make ng layers out of
        region_meshes (bool, optional, default=False):
            if True, includes a layer with the default region meshes for the volume if any exist
        seg_colors (list of str, optional, default=[]):
            Optional list of hex value colors for segments
        viewer_site (str, optional, default="default"):
            Option to override datastack's default viewer site with custom viewer site url
        custom_mesh_source (str, optional, default=None):
            If a mesh source url is given, will create a custom mesh layer
            Attempts to turn on mesh segment 1, may break if one isn't present
        custom_mesh_name str, optional, default=None):
            name for custom mesh layer
            default None will name the layer "Custom Mesh"
        custom_mesh_color (str, optional, default=None):
            color of custom mesh in hexadecimal notation starting with #
            default None will set to green "#6DB86B"
        view_coords (optional, list, default=None):
            If volume-resolution point coords are specified, will set the viewer start postiion
            default value of None will use the default start position for the chosen datastack
        long_url (bool, optional, default=False):
            optional toggle to get the default long-form NG url as output instead of using a shortened link 
        translucent_seg (bool, optional, default=False):
            if True, sets segmetnation 3D opacity to 0.99, making rendering translucent
            this is useful for doing segment proofreading comparisons, where the old seg is set to red (#FF0000)
            and the proofread seg is set to cyan (#00FFFF); this causes the overlap to turn grey, showing added
            regions as cyan and removed regions as red (any pair of directly complemetary colors can be used)

    Returns:
        output_link (str):
            the final neuroglancer link
    """

    # converts ID list to strings if ints
    if len(seg_ids) > 0 and type(seg_ids[0]) == int:
        seg_ids = list(map(str, seg_ids))

    # creates dictionary of seg-color pairs if color list was passed
    if len(seg_colors) > 0:
        color_dict = {seg_ids[i]: seg_colors[i] for i in range(len(seg_colors))}

    # pulls config dictionary for datastack from in-house list
    try:
        config = get_config(datastack=datastack)
    except KeyError:
        raise KeyError(
            "The datastack name is invalid. To see a list of currently-supported datastack names, use the get_supported_configs() function."
        )

    # sets voxel dimensions in meters
    voxel_dimensions = {
        "x": [config["resolution"][0] * 1e-9, "m"],
        "y": [config["resolution"][1] * 1e-9, "m"],
        "z": [config["resolution"][2] * 1e-9, "m"],
    }

    # handles flywire jenk for JSON syntax
    if datastack == "flywire_fafb_production":
        seg_type = "segmentation_with_graph"
        nav_dict = {
            "pose": {
                "voxelSize": voxel_dimensions,
                "voxelCoodrinates": config["default_view_point"],
            },
            "zoomFactor": 13.2,
        }
        region_alpha = 0.2
        region_color = "#808080"
    else:
        seg_type = "segmentation"
        region_alpha = 0.35
        region_color = "#f0f2f4"

    if view_coords != None:
        start_position = view_coords
    else:
        start_position = config["default_view_point"]

    # creates EM image and segmentation layer dicts
    layers = [
        {
            "type": "image",
            "name": "EM",
            "source": config["em_source_url"],
            "tab": "source",
        },
        {
            "type": seg_type,
            "name": "Segmentation",
            "source": config["seg_source_url"],
            "segments": seg_ids,
            "tab": "segments",
        },
    ]

    # changes 3d opacity to 0.99 if requested
    if translucent_seg == True:
        layers[1]["objectAlpha"] = 0.99

    # adds any annotation layers passed
    if len(anno_layers) > 0:
        for anno_layer in anno_layers:
            layers.append(anno_layer)

    # adds custom segment colors if passed
    if len(seg_colors) > 0:
        layers[1]["segmentColors"] = color_dict

    # adds region mesh layer if present
    if region_meshes == True and config["main_stack_mesh_url"] != None:
        layers.append(
            {
                "type": seg_type,
                "name": "Region Outlines",
                "source": config["main_stack_mesh_url"],
                "segments": [1],
                "segmentColors": {
                    "1": region_color,
                },
                "objectAlpha": region_alpha,
                "meshSilhouetteRendering": 2,
            }
        )

    # avoids crash if http mesh source is passed to a flywire link
    if datastack == "flywire_fafb_production" and custom_mesh_source[:4] == "http":
        print("Error: flywire doesn't support http mesh hosting")
        custom_mesh_source = None

    # is a custom mesh source url is provided, adds a custom mesh layer to the layer list
    if custom_mesh_source != None:
        if custom_mesh_name == None:
            custom_mesh_name = "Custom Mesh"
        if custom_mesh_color == None:
            custom_mesh_color = "#6DB86B"  # green#
        layers.append(
            {
                "type": seg_type,
                "name": custom_mesh_name,
                "source": custom_mesh_source,
                "segments": [1],
                "segmentColors": {"1": custom_mesh_color},
            }
        )

    # builds state dict
    # conditionally handles outdated flywire json syntax
    if datastack == "flywire_fafb_production":
        state = {
            "layers": layers,
            "navigation": nav_dict,
            "showDefaultAnnotations": False,
            "perspectiveOrientation": config["default_angle_3d"],
            "perspectiveZoom": config["default_zoom_3d"],
            "showSlices": False,
            "layout": "xy-3d",
        }
    else:
        state = {
            "dimensions": voxel_dimensions,
            "position": start_position,
            "crossSectionScale": config["default_zoom_2d"],
            "projectionOrientation": config["default_angle_3d"],
            "projectionScale": config["default_zoom_3d"],
            "layers": layers,
            "showSlices": False,
            "layout": "xy-3d",
        }

    # sets viewer site base url if none given
    if viewer_site == "default":
        viewer_site = config["viewer_site_url"]

    # handles link construction for long-form url
    if long_url == True:
        from urllib.parse import quote  # might be unnecessary #

        # json-encodes state dict
        encoded = quote(json.dumps(state, separators=(",", ":")))

        # constructs final url from viewer base and json-encoded state
        out_url = viewer_site.rstrip("/") + "/#!" + encoded

    # handles link construction for shortened url
    else:
        # sets cave client object using state dict
        client = CAVEclient(datastack)

        # uploads state to state server, gets state ID
        state_id = client.state.upload_state_json(state)

        # generates shortened url from state
        out_url = client.state.build_neuroglancer_url(state_id, viewer_site)

    return out_url


def make_objs_from_state_file(datastack, json_path, output_path):
    """
    Generates convex hull obj mesh files from all the point annotation layers in a NG state json file.

    Args:
        datastack (str):
            the name of the datastack the JSON state is from
            e.g. "brain_and_nerve_cord"
            for a list of currently-supported datastacks use get_supported_configs()
        json_path (str):
            the absolute path to the NG state JSON file to pull annotations from
            e.g. "/home/username/ng_jsons/state.json"
        output_path (str):
            the absolute path to the folder where you want to save the mesh output
            e.g. "/home/username/ng_meshes"
    """

    # gets config info dict for chosen datastack
    try:
        config = get_config(datastack=datastack)
    except KeyError:
        raise KeyError(
            "The datastack name is invalid. To see a list of currently-supported datastack names, use the get_supported_configs() function."
        )

    # adds trailing slash to output path if none present
    if output_path[-1] != "/":
        output_path += "/"

    # pulls voxel xyz dimensions from config dict
    resolution = config["resolution"]

    # opens json file and convert to python dict
    with open(json_path, "r") as json_file:
        json_dict = json.load(json_file)

    # makes empty list to fill with annotation layer names
    layer_names = []

    # gets layer names from state json file
    for layer in json_dict["layers"]:
        if "archived" not in layer:
            if layer["type"] == "annotation":
                if len(layer["annotations"]) > 0:
                    if layer["tool"] == "annotatePoint":
                        layer_names.append(layer["name"])

    # iterates through layer names and generate an obj for each
    for layer_name in layer_names:
        # extracts annotation coords as list of lists from JSON state using layer name
        points = get_anno_array_from_json_state_file(
            layer_name, json_filepath=json_path
        )

        # converts coords to numpy array  of nm-resolution point coord numpy arrays
        nm_points = np.array(
            [
                convert_coord_res(
                    point_coords=point, res_current=resolution, res_desired=[1, 1, 1]
                )
                for point in points
            ]
        )

        # creates trimesh point cloud object using xyz coor array
        point_cloud = trimesh.PointCloud(nm_points)

        # generates convex hull mesh from point cloud
        hull = point_cloud.convex_hull

        # creates obj export path from output_path
        obj_path = output_path + layer_name + ".obj"

        # saves convex hull as obj file at output path location
        hull.export(obj_path, file_type="obj")


def make_point_cloud_from_state_file(
    datastack, 
    json_filepath, 
    layer_name, 
    output_filepath,
):
    """
    Generates a point cloud OBJ file from a neuroglancer point annotation layer in a state JSON file.

    Args:
        datastack (str):
            the name of the datastack the state JSON is from
            e.g. 'brain_and_nerve_cord'
            for a list of currently-supported datastacks use get_supported_configs()
        json_filepath (str):
            the absolute path to the NG state JSON file to pull annotations from
            e.g. '/home/username/ng_jsons/state.json'
        output_filepath (str):
            the absolute path to the folder where you want to save the OBJ output file
            e.g. '/home/username/ng_meshes'
            file will be named whatever the layer name was in the state JSON
    """

    # gets config info dict for chosen datastack
    try:
        config = get_config(datastack=datastack)
    except KeyError:
        raise KeyError(
            "The datastack name is invalid. To see a list of currently-supported datastack names, use the get_supported_configs() function."
        )

    # gets resolution of volume
    resolution = config["resolution"]

    # creates numpy array of points
    points = get_anno_array_from_json_state_file(
        layer_name, json_filepath=json_filepath
    )

    # converts points to nm resolution
    nm_points = np.array(
        [
            convert_coord_res(
                point_coords=point, res_current=resolution, res_desired=[1, 1, 1]
            )
            for point in points
        ]
    )

    # creates point cloud object
    pc = trimesh.PointCloud(nm_points)

    # exports point cloud as obj
    pc.export(output_filepath, file_type="obj")


def make_volume_mesh_from_state_file(
    datastack, 
    json_filepath, 
    layer_name, 
    output_filepath, 
    export_obj=False,
):
    """
    Generates a neuroglancer volume that contains a mesh using a point annotation layer from a state JSON file. 
    
    Output will be a folder called "image" in the directory where this is run.
    Mesh is legacy-format single-resolution unsharded precomputed.
    Mesh will be convex hull, will lose concave details.

    Args:
        datastack (str):
            the name of the datastack the JSON state is from
            e.g. "brain_and_nerve_cord"
            for a list of currently-supported datastacks, use get_supported_configs()
        json_filepath (str):
            the absolute filepath to the NG state JSON file to pull annotations from
            e.g. "/home/username/ng_jsons/state.json"
        layer_name (str):
            the name of the annotation layer to pull coordinates from
            e.g. "annotation1"
        output_filepath (str):
            the absolute filepath to the folder where you want to save the mesh output
            e.g. "/home/username/ng_meshes"
        export_obj (bool, optional, default=False)
            optional toggle to export the mesh as an OBJ file in addition to making volume 
            OBJ file will save in same directory as volume as "hull.obj"
    """

    # gets config info dict for chosen datastack
    try:
        config = get_config(datastack=datastack)
    except KeyError:
        raise KeyError(
            "The datastack name is invalid. To see a list of currently-supported datastack names, use the get_supported_configs() function."
        )

    # pulls voxel xyz dimensions from config dict
    resolution = config["resolution"]

    # extracts annotation coords as list of lists from JSON state using layer name
    points = get_anno_array_from_json_state_file(
        layer_name, json_filepath=json_filepath
    )

    # converts coords to numpy array  of nm_resolution point coord numpy arrays
    nm_points = np.array(
        [
            convert_coord_res(
                point_coords=point, res_current=resolution, res_desired=[1, 1, 1]
            )
            for point in points
        ]
    )

    # creates timesh point cloud object using xyz coor array
    point_cloud = trimesh.PointCloud(nm_points)

    # generates convex hull mesh from point cloud
    hull = point_cloud.convex_hull

    # handles optional obj export
    if export_obj == True:
        # creates obj export path from output_path
        obj_filepath = output_filepath + "hull.obj"
        hull.export(obj_filepath, file_type="obj")

    # creates a folder inside the specified directory called '/image' and adds
    # an info file to it, then creates a subfolder inside image called '/mesh'
    # and adds another info file to that. This is the necessary file structure
    # for cloudvolume to create a legacy-format unsharded mesh
    make_volume_packaging(resolution=resolution, output_filepath=output_filepath)

    # constructs cloudpath from filepath
    cloudpath = "file://" + output_filepath + "/image"

    # creates cloudvolume object using information at cloudpath
    volume = cloudvolume.CloudVolume(cloudpath)

    # uses the trimesh convex hull mesh to create a cloudvolume mesh object
    cv_format_mesh = cloudvolume.Mesh(vertices=hull.vertices, faces=hull.faces)

    # gives the mesh a segment id of 1
    cv_format_mesh.segid = 1

    # adds the mesh into the volume's list of meshes, generating two files in
    # the '/image/mesh' folder, one named '1:0', called the manifest file, and
    # the other named "1:0:1.gz", called the fragment file #
    volume.mesh.put(cv_format_mesh)


def make_volume_packaging(
    output_filepath,
    resolution=[1, 1, 1],
    chunk_size=[512, 512, 16],
    volume_size=[250000, 250000, 25000],
):
    """
    Creates a file structure to hold a neuroglancer volume of legacy-format meshes in the specified directory.

    Args:
        output_filepath (str):
            absolute filepath to the folder where you want to create the mesh, e.g. 'home/username/ng_meshes" (str)
        resolution (list of ints, optional, default [1,1,1]):
            the voxel scale in nm of the datastack the mesh belongs to
            e.g. [4,4,45] for "brain_and_nerve_cord"
        chunk_size (list of ints, optional, default [512,512,16]):
            the size of the chunks in voxels for the datastack the mesh belongs to
        volume_size (list of ints, optional, default [250000,250000,25000]):
            the size of the entire volume in voxels
            e.g. [250000,250000,25000]
    """

    # sets details for cloudvolume image info file
    image_info = cloudvolume.CloudVolume.create_new_info(
        num_channels=1,
        layer_type="segmentation",
        data_type="uint64",  # channel images might be 'uint8' #
        # encoding options are raw, png, jpeg, compressed_segmentation, fpzip, kempressed, zfpc, compresso, crackle #
        encoding="raw", 
        resolution=resolution,
        voxel_offset=[0, 0, 0],  # x,y,z offset in voxels from the origin #
        mesh="mesh",
        # pick a convenient size for your underlying chunk representation #
        # powers of two are recommended, doesn't need to cover image exactly #
        chunk_size=chunk_size,
        volume_size=volume_size,
    )

    # sets details for precomputed legacy unsharded mesh info file
    mesh_info = {
        "@type": "neuroglancer_legacy_mesh",
        "transform": [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    }

    separator = "/"

    # removes trailing separator if present
    if output_filepath[-1] == separator:
        output_filepath = output_filepath[:-1]

    # sets output folder name
    volume_name = "image"

    directory_name = output_filepath + separator + volume_name

    # creates mesh subdirectory path name
    subdirectory_name = directory_name + separator + "mesh"

    # creates a directory called image in the specified directory
    try:
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # creates a directory called mesh in the image directory
    try:
        os.mkdir(subdirectory_name)
        print(f"Directory '{subdirectory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{subdirectory_name}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{subdirectory_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # saves the info dict as a JSON-formatted txt file in the image directory
    try:
        file = open((directory_name + "/info"), "wt")
        file.write(json.dumps(image_info))
        file.close()
    except Exception as e:
        print(f"An error occurred: {e}")

    # saves the info dict as a JSON-formatted txt file in the mesh directory
    try:
        file = open((subdirectory_name + "/info"), "wt")
        file.write(json.dumps(mesh_info))
        file.close()
    except Exception as e:
        print(f"An error occurred: {e}")


def triage_segs(
    datastack, 
    seg_ids, 
    return_intersects=False
):
    """
    Skeletonizes list of segs, checks if any pass through known rough spots for a given datastack. 
    
    CURRENTLY NONFUNCTIONAL: Rough spot maps are currently a work in progress.

    Args:
        datastack (str):
            the name of the datastack that contains the segments
            e.g. "brain_and_nerve_cord"
        seg_ids (list of ints):
            the ids fo the segments to check
        return_intersects (bool, optional, default=False):
            optional toggle that will return a list of all the intersection points between 
            the neuron skeletons and the rough area meshes if True, 
            otherwise returns list of True/False values for each neuron 

    Returns:
        results (list of bools OR list of (3)-shape numpy int arrays and/or None values)
            a list of True/False values for each neuron 
            OR a list of intersection points if 'return_intersects' is set to True
    """

    # gets config dict for chosen datastack
    config = get_config(datastack=datastack)

    # skeletonizes segments using id list and datastack name
    skeletons = get_seg_skeletons(datastack=datastack,seg_ids=seg_ids)

    # creates list of (n,2,3)-shape arrays of endpoint pairs for each edge in each skeleton
    catacombs = [get_bones(datastack=datastack, skeleton=skeleton) for skeleton in skeletons]

    # gets hosting url of rough spot mesh from config dict
    rough_spots = config["here_be_monsters"]

    # gets list of triangle point trio arrays from rough spot meshes
    triangles = get_mesh_triangles(volume_path=rough_spots)

    # makes empty list to populate with interseection points
    intersects = []

    # gets all intersection points for each skeleton, adds list to main 'intersects' list
    # this will add None value instead of list if no intersection points are found
    for skeleton in catacombs:
        intersections = calc_skeleton_mesh_intersect(skeleton, triangles)
        intersects.append(intersections)

    # if user requested intersection points, sets return value to intersects list
    # otherwise populates return list with True/False values for each segment
    if return_intersects == True:
        results = intersects
    else:
        results = [i != None for i in intersects]

    return results


def update_seg_list(datastack, seg_ids):
    """
    Gets the most current seg IDs for a list of seg IDs that may be outdated.

    DEPRECATION WARNING: This function can get throttled by CAVE due to an inefficiency.
    It will eventually be merged with get_current_seg_id() to become get_current_seg_ids().

    Args:
        datastack (str):
            the name of the datastack the segment ids are from
        seg_ids (list of ints):
            a list of segment ids you want to update

    Returns:
        fresh_segs (list of ints):
            a list of current seg ids
    """

    # prints deprecation warning
    print("DEPRECATION WARNING: This function can get throttled by CAVE due to an inefficiency.") 
    print("It will eventually be merged with get_current_seg_id() to become get_current_seg_ids().")

    # make df with columns for stale segs and T/F result of freshness checker
    df = pd.DataFrame(
        {"stale_seg": seg_ids, "already_fresh": check_seg_freshness(datastack, seg_ids)}
    )

    # make empty list to fill with current seg ids #
    fresh_segs = []

    # if seg is already fresh, add to list, otherwise use freshener
    for seg_id in seg_ids:
        if df.loc[df["stale_seg"] == seg_id, "already_fresh"].values[0] == True:
            fresh_segs.append(seg_id)
        else:
            fresh_segs.append(get_current_seg_id(datastack=datastack, seg_id=seg_id))

    return fresh_segs


def visualize_skeletons(seg_ids, datastack="brain_and_nerve_cord"):
    """
    Generate a microviewer window using the submitted segment IDs.

    Currently only works with BANC.

    Args:
        seg_ids (list of ints):
            a list of segment IDs to visualize
        datastack (str, optional, default="brain_and_nerve_cord"):
            the name of the datastack the segment IDs come from
            currently only "brain_and_nerve_cord" is supported
    """

    # sets client
    client = CAVEclient(datastack)

    # creates 32-bit float array for volume resolution
    matrix = np.array(
        [
            [16, 0, 0, 0],
            [0, 16, 0, 0],
            [0, 0, 45, 0],
        ],
        dtype=np.float32,
    )

    # sends request to generate skeletons to skeletonization service
    # gets back time estimate for skeletonization process
    seconds = client.skeleton.generate_bulk_skeletons_async(
        seg_ids, skeleton_version=-1
    )

    # if seconds returns a dictionary, a bad ID was passed, exits
    if isinstance(seconds, dict):
        print("Bad segment id.")
        sys.exit(0)

    # prints time estimate
    print(f"ETA {seconds} seconds.")

    # waits the suggested number of seconds before continuing to give skeletons time to generate
    time.sleep(seconds)

    # pulls list of generated skeletons from service
    cskel_list = [client.skeleton.get_skeleton(i) for i in seg_ids]

    # converts cave skeletons to osteoid skeletons
    pskel_list = [
        Skeleton(
            vertices=c["vertices"],
            edges=c["edges"],
            radii=c["radius"],
            transform=matrix,
            space="physical",
        )
        for c in cskel_list
    ]

    # initiates microviewer and feeds in skeletons
    viewer_list = pskel_list
    microviewer.objects(viewer_list)
