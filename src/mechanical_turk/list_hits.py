from utils import get_mt_client



client = get_mt_client()
hits = client.list_hits()
assignment_res = client.list_assignments_for_hit(HITId='386T3MLZMVE18Q1H6D1UGEW6KQY08O')
a = 0