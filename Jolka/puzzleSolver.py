from pytictoc import TicTocGenerator, tic, toc


def printBoard():
    partial = []
    for i in range(n):
        partial.append("".join(board[i]))
    psolution = "\n".join(partial)
    print(psolution)
    print("***************")


def find():
    if plan == []:
        if hLeft == []:
            if vLeft == []:
                return True
            plan.append((1, vLeft[0]))
        else:
            plan.append((0, hLeft[0]))

    #    printBoard()

    hv, widx = plan.pop(0)
    gap = gaps[hv][widx]
    domain = words[gap[3]].copy()
    nop = len(plan)

    if hv == 0:
        i = gap[0]
        for j in range(gap[1], gap[2]):
            if board[i][j] == "_":
                continue
            k = j - gap[1]
            fits = []
            for word in domain:
                if word[k] == board[i][j]:
                    fits.append(word.strip())
            domain = fits

        if domain == []:
            return False

        for word in domain:
            # !!! new line
            words[gap[3]].remove(word)

            idx = hLeft.index(widx)
            del hLeft[idx]
            temp = []
            for j in range(gap[1], gap[2]):
                c = cells[(i, j)][1]
                if c != -1 and c in vLeft and (1, c) not in plan:
                    plan.append((1, c))
                k = j - gap[1]
                temp.append(board[i][j])
                board[i][j] = word[k]
            if find():
                return True
            # !!! new line
            words[gap[3]].append(word)

            for j in range(gap[1], gap[2]):
                k = j - gap[1]
                board[i][j] = temp[k]
            hLeft.insert(idx, widx)
            while len(plan) > nop:
                del plan[-1]

        return False

    else:
        j = gap[1]
        for i in range(gap[0], gap[2]):
            if board[i][j] == "_":
                continue
            k = i - gap[0]
            fits = []
            for word in domain:
                if word[k] == board[i][j]:
                    fits.append(word.strip())
            domain = fits

        if domain == []:
            return False

        for word in domain:
            # !!! new line
            words[gap[3]].remove(word)

            idx = vLeft.index(widx)
            del vLeft[idx]
            temp = []
            for i in range(gap[0], gap[2]):
                c = cells[(i, j)][0]
                if c != -1 and c in hLeft and (0, c) not in plan:
                    plan.append((0, c))
                k = i - gap[0]
                temp.append(board[i][j])
                board[i][j] = word[k]
            if find():
                return True

            # !!! new line
            words[gap[3]].append(word)

            for i in range(gap[0], gap[2]):
                k = i - gap[0]
                board[i][j] = temp[k]
            vLeft.insert(idx, widx)
            while len(plan) > nop:
                del plan[-1]

        return False


###################


TicToc = TicTocGenerator()

for problem in [3]:  # [0,1,2,4]: #range(5):
    with open("./Jolka/puzzle" + str(problem)) as f:
        board = f.readlines()

    with open("./Jolka/words" + str(problem)) as f:
        rawWords = f.readlines()

    tic(TicToc)

    words = {}

    for word in rawWords:
        n = len(word.strip())
        if n not in words.keys():
            words[n] = []
        words[n].append(word.strip())

    n = len(board)

    for i in range(n):
        board[i] = list(board[i].strip())

    m = len(board[0])

    cells = {}

    horGaps = []

    for i in range(n):
        j = 0
        while j < m:
            while j < m and board[i][j] == "#":
                j += 1
            k = j

            while j < m and board[i][j] == "_":
                j += 1
            if j - k > 1:
                for c in range(k, j):
                    cells[(i, c)] = [len(horGaps), -1]
                horGaps.append((i, k, j, j - k, 0))
            else:
                cells[(i, j)] = [-1, -1]

    verGaps = []

    for i in range(m):
        j = 0
        while j < n:
            while j < n and board[j][i] == "#":
                j += 1
            k = j

            while j < n and board[j][i] == "_":
                j += 1
            if j - k > 1:
                for c in range(k, j):
                    cells[(c, i)][1] = len(verGaps)
                verGaps.append((k, i, j, j - k, 1))

    gaps = []
    gaps.append(horGaps)
    gaps.append(verGaps)

    hLeft = list(range(len(horGaps)))
    vLeft = list(range(len(verGaps)))

    plan = [(1, 9)]  # , (1,15), (1,21), (1,31)]

    result = find()
    elapse = toc(TicToc)
    print(f"Problem {problem} has solution: {result} elapsed time: {elapse}")

    for i in range(n):
        board[i] = "".join(board[i])

    solution = "\n".join(board)

    with open("./Jolka/solution" + str(problem), "w") as f:
        f.writelines(solution)
        f.write("\n" + str(elapse))
