Details
The functions should do the following:

• def insert(self, key: int):

Insert the key into the tree and rebalance as per B-tree rules. The key is guaranteed not to be
in the tree.

• def delete(self, key: int):

Delete the key from the tree and rebalance as per B-tree rules. The key is guaranteed to be in
the tree.

• def search(self, key: int):

Calculate the list of child indices followed on the path from the root to the node which includes
the key. If the key is in the root, return []. The key is guaranteed to be in the tree.

Order of Operations

For insertion, follow these steps when correcting an overfull node:

1. Use a left rotation if possible and effective.

2. Use a right rotation if possible and effective.

3. Split.

For deletion, follow these steps when correcting an underful node:

1. Use a right rotation if possible and effective.

2. Use a left rotation if possible and effective.

3. Merge with left sibling if possible and effective.

4. Merge with right sibling if possible and effective.


