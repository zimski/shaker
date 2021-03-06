NEXT_VMID=$(pvesh get cluster/nextid | sed 's/"//g')
mkdir /var/lib/vz/images/$NEXT_VMID
% if env['vm']['kernel'] == 3.11 :
cp /var/lib/vz/images/111/base-111-disk-1.qcow2 /var/lib/vz/images/$NEXT_VMID/base-$NEXT_VMID-disk-1.qcow2
% elif env['vm']['kernel'] == 3.8:
cp /var/lib/vz/images/116/base-116-disk-1.qcow2 /var/lib/vz/images/$NEXT_VMID/base-$NEXT_VMID-disk-1.qcow2
% endif
pvesh create /nodes/proxmox/qemu -vmid $NEXT_VMID -memory 2048 -sockets 1 -cores 2 -net0 e1000=${env['vm']['mac']},bridge=vmbr0 -ide0=local:$NEXT_VMID/base-$NEXT_VMID-disk-1.qcow2
echo "vm created"
$$ sk_console.get GET_VAR
$$ rbox.py_run UPDATE_VM_ID
sleep 5 ; pvesh create /nodes/proxmox/qemu/$NEXT_VMID/status/start