\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  x[1,2] + 3 x[1,3] + 2 x[1,4] + 2 x[2,1] + x[2,3] + 3 x[2,4] + 3 x[3,1]
   + 2 x[3,2] + x[3,4] + x[4,1] + 3 x[4,2] + 2 x[4,3]
Subject To
 node_flow_1: x[1,2] + x[1,3] + x[1,4] - x[2,1] - x[3,1] - x[4,1] = 0
 node_out_1: x[1,2] + x[1,3] + x[1,4] = 1
 node_flow_2: - x[1,2] + x[2,1] + x[2,3] + x[2,4] - x[3,2] - x[4,2] = 0
 node_out_2: x[2,1] + x[2,3] + x[2,4] = 1
 node_flow_3: - x[1,3] - x[2,3] + x[3,1] + x[3,2] + x[3,4] - x[4,3] = 0
 node_out_3: x[3,1] + x[3,2] + x[3,4] = 1
 node_flow_4: - x[1,4] - x[2,4] - x[3,4] + x[4,1] + x[4,2] + x[4,3] = 0
 node_out_4: x[4,1] + x[4,2] + x[4,3] = 1
 time_12: 100 x[1,2] + s[1] - s[2] <= 99
 time_13: 100 x[1,3] + s[1] - s[3] <= 97
 time_14: 100 x[1,4] + s[1] - s[4] <= 98
 time_23: 100 x[2,3] + s[2] - s[3] <= 98
 time_24: 100 x[2,4] + s[2] - s[4] <= 99
 time_32: 100 x[3,2] - s[2] + s[3] <= 97
 time_34: 100 x[3,4] + s[3] - s[4] <= 97
 time_42: 100 x[4,2] - s[2] + s[4] <= 98
 time_43: 100 x[4,3] - s[3] + s[4] <= 99
Bounds
 s[1] <= 100
 s[2] <= 100
 s[3] <= 100
 s[4] <= 100
Binaries
 x[1,2] x[1,3] x[1,4] x[2,1] x[2,3] x[2,4] x[3,1] x[3,2] x[3,4] x[4,1]
 x[4,2] x[4,3]
Generals
 s[1] s[2] s[3] s[4]
End
