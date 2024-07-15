import bpy

bpy.ops.outliner.orphans_purge(do_local_ids=do_local_ids, do_linked_ids=do_linked_ids, do_recursive=do_recursive)

# Optional: Set arguments here (default: all True)
local_ids = True
linked_ids = True
recursive = True

# Execute the purge function
purge_orphans(local_ids, linked_ids, recursive)
