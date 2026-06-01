from strawberry_fertigation_calculator import StrawberryFertigationCalculator

calc = StrawberryFertigationCalculator()

# Calculate requirements for Stage 3 (Expansion) targeting a 500L field tank
# 计算第 3 阶段（膨大期）配制 500L 营养液所需的原料用量
result = calc.calculate(stage_id=3, target_volume_l=500.0)

# Render formatted batch sheet to standard output
# 打印标准配料单
calc.print_recipe(result)
