def safe_get(arr, index, default=None):
    sliced = arr[index:index+1]
    return sliced[0] if sliced else default
