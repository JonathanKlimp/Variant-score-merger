from itertools import groupby

score_groups = {
    0.5: "low",
    0.7: "low",
    0.8: "medium",
    0.9: "medium",
    0.95: "high"
}

class BedRecord(object):
    group_score = ""

    def __init__(self, chr, pos, nuc, alt, score):
        self.chr = chr
        self.pos = pos
        self.nuc = nuc
        self.alt = alt
        self.score = float(score)
    
    def get_score_group(self):
        if self.group_score == "":
            # print(self.score)
            # print(type(self.score))
            # print(self.score <= 0.7)
            # print(self.score > 0.9)
            if self.score <= 0.7:
                self.group_score = "low"
            elif self.score > 0.7 and self.score <= 0.9:
                self.group_score = "medium"
            elif self.score > 0.9:
                self.group_score = "high"  
            else:
                self.group_score = "low"  
            return self.group_score
        else:
            return self.group_score      


def parse_records(in_file):
    with open(in_file) as f:
        for line in f:
            yield BedRecord(*line.strip().split())


def merge_groups(group):
    output = [next(group)]
    output[-1].get_score_group()
    for record in group:
        print(record.get_score_group())
        if record.pos <= output[-1].pos and record.group_score == output[-1].group_score:
            output[-1].pos = max(output[-1].pos, record.pos)
        else:
            output.append(record)
    return output

def main(in_file):
    for _, group in groupby(parse_records(in_file), lambda x: (x.chr, x.score)):
        for r in merge_groups(group):
            print('\t'.join([r.chr, r.pos, r.nuc, r.alt, r.group_score]))

if __name__ == '__main__':
    main('GRCh37_fathmm_MKL_scores_copy.tsv')