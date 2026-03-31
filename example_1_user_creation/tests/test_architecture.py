from pytest_archon import archrule

# Since your path is .../example_1_user_creation,
# and your folders are l1_entities, l2_use_cases, etc.
# If you run pytest from inside 'example_1_user_creation', BASE is empty.
BASE_PACKAGE = "example_1_user_creation"


def test_clean_architecture_layers():
    # 1. Entities (L1) isolation
    # It should not know about ANY other internal layer.
    archrule("Entities isolation").match(f"{BASE_PACKAGE}.l1_entities*").should_not_import(
        f"{BASE_PACKAGE}.l2_use_cases*",
    ).should_not_import(f"{BASE_PACKAGE}.l3_interface_adapters*").should_not_import(
        f"{BASE_PACKAGE}.l4_frameworks_and_drivers*",
    ).check(BASE_PACKAGE)

    # 2. Use Cases (L2) isolation
    # It can import L1, but NOT L3 or L4.
    archrule("Use Cases isolation").match(f"{BASE_PACKAGE}.l2_use_cases*").should_not_import(
        f"{BASE_PACKAGE}.l3_interface_adapters*",
    ).should_not_import(f"{BASE_PACKAGE}.l4_frameworks_and_drivers*").check(BASE_PACKAGE)

    # 3. Interface Adapters (L3) isolation
    # It can import L1 and L2, but NOT L4.
    archrule("Interface Adapters isolation").match(f"{BASE_PACKAGE}.l3_interface_adapters*").should_not_import(
        f"{BASE_PACKAGE}.l4_frameworks_and_drivers*",
    ).check(BASE_PACKAGE)
