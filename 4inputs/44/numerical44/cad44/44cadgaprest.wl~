(* ::Package:: *)

perm2expr[perm_,polys_]:=Module[{temp,ret},temp =Table[polys[[perm[[kk]]]] < polys[[perm[[kk+1]]]] , {kk,1,Length[perm]-1}] ; ret=And@@temp;Return[ret];]
usecad[perm_,polys_,restrictions_,vars_]:=Module[{expr,ret},
expr = Simplify[perm2expr[perm,polys]\[And]restrictions];
ret =FindInstance[expr,Evaluate[vars]];
Return[ret];]
usereduce[perm_,polys_,restrictions_,bvars_,fvars_]:=Module[{expr,ret,exist},
expr = Simplify[perm2expr[perm,polys]\[And]restrictions];
exist =Exists[Evaluate[bvars],expr];
ret = Reduce[exist,Evaluate[fvars]];
Return[ret];
]

run44[timebound_]:=Module[{componentone,componenttwo,bvars,fvars,instance,asymmetricorders,polys,restrictions,ret,bound},
SetDirectory["/home/lz210/cad44"];
componentone=(1+Sum[\[Delta][k],{k,#}])&/@Subsets[Table[kk,{kk,3,4}]];
componenttwo = (1+Sum[\[Delta][k],{k,#}])&/@Subsets[Table[kk,{kk,1,2}]];
restrictions = 0< \[Delta][1] < \[Delta][2]\[And]0< \[Delta][3] < \[Delta][4];
polys = Flatten[Table[i*j,{i,componentone},{j,componenttwo}]];

asymmetricorders = Import["gap44.json","JSON"];
bound=Length[asymmetricorders];
ret={};
bvars = {\[Delta][1],\[Delta][2]};
fvars = {\[Delta][3],\[Delta][4]};
Timing[For[i=1,i<=bound,i++,instance=TimeConstrained[usereduce[asymmetricorders[[i]]+1,polys,restrictions,bvars,fvars],timebound];Print[{i,instance}];If[instance ==False,AppendTo[ret,i],None];];];

bvars = {\[Delta][3],\[Delta][4]};
fvars = {\[Delta][1],\[Delta][2]};
Timing[For[i=1,i<=bound,i++,instance=TimeConstrained[usereduce[asymmetricorders[[i]]+1,polys,restrictions,bvars,fvars],timebound];Print[{i,instance}];If[instance ==False,AppendTo[ret,i],None];];];
nodret = DeleteDuplicates[ret];
Export["nodret3s.json",nodret];
]
