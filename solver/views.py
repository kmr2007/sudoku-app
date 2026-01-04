from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .puzzle import Puzzle

# Views
def index(request):
    template = loader.get_template("solver/index.html")
    if request.method == "POST":
        # parse input
        pzl = []
        for r in range(9):
            row = []
            for c in range(9):
                val = request.POST[f"{r}-{c}"]
                if val == "":
                    row.append("?")
                else:
                    row.append(int(val))
            pzl.append(row)
        pzl = Puzzle(pzl)
        
        # solve puzzle
        if pzl.isFailed():
            context = {
                    "puzzle": pzl.state,
                    "status": "invalid"
                }
        else:
            pzl.removeSingles()
            solution = pzl.solve()
            if solution is None:
                context = {
                    "puzzle": pzl.state,
                    "status": "unsolvable"
                }
            else:
                pzl = solution
                # output solved puzzle
                context = {
                    "puzzle": pzl.state,
                    "status": "solved"
                }
    else:
        pzl = []
        for r in range(9):
            row = []
            for c in range(9):
                row.append("?")
            pzl.append(row)
        pzl = Puzzle(pzl)
        context = {
            "puzzle": pzl.state,
            "status": "input"}
    
    return HttpResponse(template.render(context, request))


    