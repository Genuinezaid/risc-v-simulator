class HazardDetector:
    def __init__(self):
        self.hazards_detected = 0

    def detect_hazards(self, pipeline):
        id_inst = pipeline['ID'].get('instruction')
        if not id_inst:
            return None


        if pipeline['EX'].get('instruction'):
            ex_rd = pipeline['EX']['rd']
            if ex_rd != 0 and (ex_rd == pipeline['ID']['rs1'] or
                               ex_rd == pipeline['ID']['rs2']):
                if pipeline['EX']['instruction']['op'].startswith('l'):
                    return 'Load-use data hazard'
                return 'Data hazard (forwarding possible)'


        if id_inst['op'].startswith('b') or id_inst['op'] in ['jal', 'jalr']:
            return 'Control hazard (branch/jump)'

        return None

    def get_operands_with_forwarding(self, inst, ex_stage, mem_stage, registers):

        op1 = inst['rs1Val']
        op2 = inst['rs2Val']


        if ex_stage.get('instruction') and ex_stage['rd'] == inst['rs1'] and ex_stage['rd'] != 0:
            op1 = ex_stage['aluResult']

        if ex_stage.get('instruction') and ex_stage['rd'] == inst['rs2'] and ex_stage['rd'] != 0:
            op2 = ex_stage['aluResult']



        return op1, op2