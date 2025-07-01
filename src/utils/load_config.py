from pathlib import Path
import src.utils.general as utils

current_file_path = Path(__file__)
main_directory = current_file_path.parents[2]
config_path = main_directory.joinpath("src/utils/config.yml")

### Glossary of symbols for variables
# c = category
# ch = checklist
# d = dropdown
# f = filter
# fl = floor
# i = impact
# ln = line
# m = material
# nm = name
# no = normalization
# t = toggle
# typ = type
# p = project
# lcs = life cycle stage
# out = outlier
# sc = scope
# sort = sort
# v = values

app_config = utils.read_yaml(config_path)
assert app_config is not None, "The app_config dictionary could not be set"

impact_dropdown_yaml = app_config.get("i_d")
assert (
    impact_dropdown_yaml is not None
), "The app_config for total impacts could not be set"

impact_type_radio_yaml = app_config.get("i_typ")
assert (
    impact_type_radio_yaml is not None
), "The app_config for impact type radio could not be set"

lcs_checklist_yaml = app_config.get("lcs_c")
assert (
    lcs_checklist_yaml is not None
), "The app_config for lcs checklist could not be set"

scope_checklist_yaml = app_config.get("sc_c")
assert (
    scope_checklist_yaml is not None
), "The app_config for scope checklist could not be set"

proj_type_checklist_yaml = app_config.get("p_typ_c")
assert (
    proj_type_checklist_yaml is not None
), "The app_config for proj_type checklist could not be set"

categorical_toggle_one_yaml = app_config.get("c_t_1")
assert (
    categorical_toggle_one_yaml is not None
), "The app_config for categorical selection toggle could not be set"

categorical_dropdown_one_yaml = app_config.get("c_d_1")
assert (
    categorical_dropdown_one_yaml is not None
), "The app_config for cat. dropdowns could not be set"

categorical_filter_toggle_one_yaml = app_config.get("c_f_t_1")
assert (
    categorical_filter_toggle_one_yaml is not None
), "The app_config for cat. dropdowns could not be set"

categorical_filter_one_yaml = app_config.get("c_f_1")
assert (
    categorical_filter_one_yaml is not None
), "The app_config for cat filters could not be set"

categorical_toggle_two_yaml = app_config.get("c_t_2")
assert (
    categorical_toggle_two_yaml is not None
), "The app_config for second cat select could not be set"

categorical_dropdown_two_yaml = app_config.get("c_d_2")
assert (
    categorical_dropdown_two_yaml is not None
), "The app_config for second cat dropdown could not be set"

categorical_filter_toggle_two_yaml = app_config.get("c_f_t_2")
assert (
    categorical_filter_toggle_two_yaml is not None
), "The app_config for second cat filter toggle could not be set"

categorical_filter_two_yaml = app_config.get("c_f_2")
assert (
    categorical_filter_two_yaml is not None
), "The app_config for second cat filters could not be set"

material_filter_toggle_yaml = app_config.get("m_t")
assert (
    material_filter_toggle_yaml is not None
), "The app_config for material filter toggle could not be set"

material_filter_yaml = app_config.get("m_f")
assert (
    material_filter_yaml is not None
), "The app_config for material filters could not be set"

floor_area_normalization_radio_yaml = app_config.get("fl_no")
assert (
    floor_area_normalization_radio_yaml is not None
), "The app_config for floor area norm. could not be set"

sort_values_radio_yaml = app_config.get("sort_v")
assert (
    sort_values_radio_yaml is not None
), "The app_config for box plot sorting could not be set"

outlier_toggle_yaml = app_config.get("out_t")
assert (
    outlier_toggle_yaml is not None
), "The app_config for outlier toggle could not be set"

line_toggle_yaml = app_config.get("ln_t")
assert line_toggle_yaml is not None, "The app_config for line toggle could not be set"

line_value_yaml = app_config.get("ln_v")
assert (
    line_value_yaml is not None
), "The app_config for line number input could not be set"

line_name_yaml = app_config.get("ln_nm")
assert line_name_yaml is not None, "The app_config for line name input could not be set"

field_name_map = app_config.get("field_name_map")
assert field_name_map is not None, "The app_config for field names could not be set"

category_order_map = app_config.get("category_order_map")
assert (
    category_order_map is not None
), "The app_config for category orders could not be set"

caption_orders = app_config.get("caption_orders")
assert caption_orders is not None, "The app_config for caption orders could not be set"

material_list = app_config.get("material_list")
assert material_list is not None, "The app_config for caption orders could not be set"
