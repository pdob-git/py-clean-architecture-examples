from pytest_archon import archrule

# In this project, the layers are direct subdirectories of example_1_user_creation.
# When running pytest from the root, the package prefix is the folder name.
BASE = "example_1_user_creation"


def test_clean_architecture_dependency_rules():
    """
    Enforces the 'Dependency Rule': Source code dependencies can only
    point inwards, toward higher-level policies (Entities).
    """

    # --- RULE 1: Entities (L1) are the core ---
    # They must have ZERO dependencies on any other internal layers.
    archrule("L1 Entities: Absolute Isolation").match(f"{BASE}.l1_entities*").should_not_import(
        f"{BASE}.l2_use_cases*",
    ).should_not_import(f"{BASE}.l3_interface_adapters*").should_not_import(f"{BASE}.l4_frameworks_and_drivers*").check(
        BASE,
    )

    # --- RULE 2: Use Cases (L2) ---
    # Can import L1, but nothing 'outer' (L3 or L4).
    archrule("L2 Use Cases: Inner Only").match(f"{BASE}.l2_use_cases*").should_not_import(
        f"{BASE}.l3_interface_adapters*",
    ).should_not_import(f"{BASE}.l4_frameworks_and_drivers*").check(BASE)

    # --- RULE 3: Interface Adapters (L3) ---
    # Can import L1 and L2 (the core), but not the 'Infrastructure' (L4).
    archrule("L3 Interface Adapters: No Frameworks").match(f"{BASE}.l3_interface_adapters*").should_not_import(
        f"{BASE}.l4_frameworks_and_drivers*",
    ).check(BASE)

    # --- RULE 4: Frameworks & Drivers (L4) ---
    # No specific 'should_not_import' as it is the outermost layer,
    # but we check it for cycles to ensure healthy glue code.
    archrule("L4 Frameworks: No Cycles").match(f"{BASE}.l4_frameworks_and_drivers*").should_not_import(
        f"{BASE}.l4_frameworks_and_drivers*",
    ).check(BASE, skip_type_checking=True)
    # Note: We don't usually restrict L4 imports since it's the 'Main' entry point.
